import argparse
from pathlib import Path
import json
import time
import numpy as np
from scipy.signal import lfilter, lfilter_zi
from sklearn.linear_model import Ridge
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.pipeline import make_pipeline
from threadpoolctl import threadpool_limits
from .data import ROOT, INPUTS, TARGETS, IQ, get_profiles, SEED

SCENARIOS = ["clean","random_missing","outage","bias","drift","noise"]
LEVELS = [.5,.8,.9,.95]
HOT = 80.0  # descriptive, not a material/safety limit

def condition(x, pid, scenario, scale):
    out=x.copy()
    rng=np.random.default_rng(SEED+pid)
    start=len(x)//3
    end=2*len(x)//3
    if scenario=="random_missing": out[rng.random(len(x))<.20,IQ]=np.nan
    if scenario=="outage": out[start:end,IQ]=np.nan
    if scenario=="bias": out[start:,IQ]+=scale
    if scenario=="drift": out[start:,IQ]+=np.linspace(0,scale,len(x)-start)
    if scenario=="noise": out[:,IQ]+=rng.normal(0,scale*.25,len(x))
    active=np.zeros(len(x),dtype=bool)
    if scenario=="random_missing": active=~np.isfinite(out[:,IQ])
    elif scenario=="outage": active[start:end]=True
    elif scenario in ("bias","drift"): active[start:]=True
    elif scenario=="noise": active[:]=True
    return out,active

def forward_fill(x, median):
    filled=x.copy()
    for j in range(x.shape[1]):
        col=x[:,j]
        prev=np.maximum.accumulate(np.where(np.isfinite(col),np.arange(len(col)),-1))
        filled[:,j]=np.where(prev>=0,col[np.maximum(prev,0)],median[j])
    return filled

def proxies(x):
    a,b,ud,uq,s,id_,iq=x.T
    return np.c_[x,np.abs(s),id_**2+iq**2,np.abs(ud*id_+uq*iq),ud**2+uq**2]

def features(x,dt,derived=True):
    p=proxies(x) if derived else x
    filtered=[]
    for tau in [60,600,1800]:
        a=float(np.exp(-dt/tau))
        b=[1-a]
        den=[1,-a]
        start=lfilter_zi(b,den)[:,None]*p[0]
        filtered.append(lfilter(b,den,p,axis=0,zi=start)[0])
    return np.column_stack([p,*filtered])

def basic(y,p,active):
    e=np.abs(y-p)
    def sub(mask):
        return dict(n=int(mask.sum()),mae=float(e[mask].mean()) if mask.any() else None,
                    rmse=float(np.sqrt(np.mean(e[mask]**2))) if mask.any() else None)
    idx=int(e.argmax())
    return dict(n=len(e),mae=float(e.mean()),rmse=float(np.sqrt(np.mean(e**2))),
        maxae=float(e[idx]),worst_sample=idx,worst_measured=float(y[idx]),worst_predicted=float(p[idx]),
        hot=sub(y>=HOT),active=sub(active))

def aggregate(rows):
    total=sum(r["n"] for r in rows)
    def subsets(key):
        count=sum(r[key]["n"] for r in rows)
        return dict(n=count,mae=sum(r[key]["n"]*(r[key]["mae"] or 0) for r in rows)/count if count else None,
                    rmse=float(np.sqrt(sum(r[key]["n"]*(r[key]["rmse"] or 0)**2 for r in rows)/count)) if count else None)
    return dict(mae=sum(r["mae"]*r["n"] for r in rows)/total,
        rmse=float(np.sqrt(sum(r["rmse"]**2*r["n"] for r in rows)/total)),
        maxae=max(r["maxae"] for r in rows),macro_mae=float(np.mean([r["mae"] for r in rows])),
        hot=subsets("hot"),active=subsets("active"))

def profile_conformal(abs_residual_by_profile,level):
    vals=sorted(float(np.max(x)) for x in abs_residual_by_profile)
    rank=int(np.ceil((len(vals)+1)*level))
    return vals[rank-1] if rank<=len(vals) else None

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--ridge-only",action="store_true")
    ap.add_argument("--stride",type=int,default=20)
    ap.add_argument("--epochs",type=int,default=10)
    opt=ap.parse_args()
    dt=.5*opt.stride
    sets,data=get_profiles(opt.stride)
    xtrain=np.concatenate([data[i][0] for i in sets["train"]])
    median=np.median(xtrain,axis=0)
    scale=float(xtrain[:,IQ].std())
    other=np.arange(len(INPUTS))!=IQ
    imputer=make_pipeline(PolynomialFeatures(2,include_bias=False),StandardScaler(),Ridge(alpha=10))
    imputer.fit(xtrain[:,other],xtrain[:,IQ])
    xall=np.concatenate([features(data[i][0],dt) for i in sets["train"]])
    ridge=make_pipeline(StandardScaler(),Ridge(alpha=30)).fit(xall,np.concatenate([data[i][1][:,0] for i in sets["train"]]))
    ridge_plain=make_pipeline(StandardScaler(),Ridge(alpha=30)).fit(
        np.concatenate([features(data[i][0],dt,False) for i in sets["train"]]),
        np.concatenate([data[i][1][:,0] for i in sets["train"]]))
    print(f"Ridge fitted; {xall.shape[0]} train samples. i_q train SD={scale:.2f}",flush=True)
    models={"Ridge": (lambda x:ridge.predict(features(x,dt)),len(ridge[-1].coef_)+1,False),
        "Ridge_plain": (lambda x:ridge_plain.predict(features(x,dt,False)),len(ridge_plain[-1].coef_)+1,False)}
    details={}
    if not opt.ridge_only:
        from .tnn import fit_tnn
        tnn,n,details["TNN"]=fit_tnn(data,sets,dt,opt.epochs,signed=False)
        signed,n_signed,details["TNN_signed_ablation"]=fit_tnn(data,sets,dt,opt.epochs,signed=True)
        models.update(TNN=(tnn,n,False),TNN_signed_ablation=(signed,n_signed,False),
                      TNN_reconstruct=(tnn,n+len(imputer[-1].coef_)+1,True))

    results=dict(split=sets,stride=opt.stride,dt=dt,high_temperature_c=HOT,iq_train_sd_a=scale,
                 sensors=INPUTS,targets=TARGETS,epochs=opt.epochs,model_fits=details,models={})
    replay={}
    for name,(predict,n,restore) in models.items():
        def infer(pid,scenario):
            raw,y=data[pid]
            seen,active=condition(raw,pid,scenario,scale)
            t=time.perf_counter()
            filled=forward_fill(seen,median)
            missing=~np.isfinite(seen[:,IQ])
            if restore and missing.any():
                filled[missing,IQ]=imputer.predict(filled[missing][:,other])
            p=predict(filled)
            assert len(p)==len(y) and np.isfinite(p).all()
            return y[:,0],p,active,(time.perf_counter()-t)*1000/len(y)
        cal_clean=[np.abs(y-p) for pid in sets["calibration"] for y,p,*_ in [infer(pid,"clean")]]
        cal_missing=[np.concatenate([np.abs(y-p) for case in ("random_missing","outage")
            for y,p,*_ in [infer(pid,case)]]) for pid in sets["calibration"]] if restore else cal_clean
        def calibrate(rows):
            return np.quantile(np.concatenate(rows),LEVELS,method="higher").tolist()
        widths={"clean":calibrate(cal_clean),"known_missing":calibrate(cal_missing)}
        blocks=dict(trainable_coefficients=n,half_widths_c=widths,
                    clean_profile_simultaneous_90=profile_conformal(cal_clean,.9),scenarios={})
        for case in SCENARIOS:
            w=widths["known_missing" if case in ("random_missing","outage") else "clean"]
            rows={}
            traces={}
            for pid in sets["test"]:
                y,p,active,latency=infer(pid,case)
                m=basic(y,p,active)
                m["coverage"]=[float(np.mean(np.abs(y-p)<=d)) for d in w]
                m["coverage_using_clean_90"]=float(np.mean(np.abs(y-p)<=widths["clean"][2]))
                m["profile_simultaneous_90_pass"]=bool(m["maxae"]<=blocks["clean_profile_simultaneous_90"])
                m["cpu_ms_per_sample"]=latency
                rows[str(pid)]=m
                x,_=data[pid]
                seen,_=condition(x,pid,case,scale)
                traces[str(pid)]=dict(y=np.round(y,3).tolist(),prediction=np.round(p,3).tolist(),
                    speed=np.round(x[:,INPUTS.index("motor_speed")],2).tolist(),
                    coolant=np.round(x[:,INPUTS.index("coolant")],2).tolist(),
                    iq=[round(float(v),2) if np.isfinite(v) else None for v in seen[:,IQ]],
                    active=active.astype(int).tolist(),half_width=w[2])
            values=list(rows.values())
            total=sum(r["n"] for r in values)
            cov=[sum(r["coverage"][i]*r["n"] for r in values)/total for i in range(len(LEVELS))]
            blocks["scenarios"][case]=dict(**aggregate(values),coverage_levels=LEVELS,coverage=cov,
                mean_absolute_coverage_error=float(np.mean(np.abs(np.array(cov)-LEVELS))),
                coverage_using_clean_90=sum(r["n"]*r["coverage_using_clean_90"] for r in values)/total,
                profile_simultaneous_90_passes=sum(r["profile_simultaneous_90_pass"] for r in values),
                interval_width_c=2*w[2],cpu_ms_per_sample_median=float(np.median([r["cpu_ms_per_sample"] for r in values])),profiles=rows)
            replay.setdefault(name,{})[case]=traces
            print(f"{name:22} {case:15} MAE {blocks['scenarios'][case]['mae']:.3f} cover90 {cov[2]:.3f}",flush=True)
        results["models"][name]=blocks
    dest=ROOT/"results"
    dest.mkdir(exist_ok=True)
    suffix="-ridge" if opt.ridge_only else ""
    (dest/f"experiment{suffix}.json").write_text(json.dumps(results,indent=2,allow_nan=False),encoding="utf-8")
    (dest/f"replay{suffix}.json").write_text(json.dumps(replay,separators=(",",":"),allow_nan=False),encoding="utf-8")

if __name__=="__main__":
    with threadpool_limits(limits=1):
        main()
