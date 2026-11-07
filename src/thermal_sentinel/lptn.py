"""Effective 1-node thermal-network negative control, NOT physical R/C identification.

Paderborn only. Uses frozen complete-profile split and native-stride protocol.
No CREATOR power is transferred to this different motor; no measured test target
is used for initialization or recurrent state updates.
"""
from pathlib import Path
import sys
import json
import hashlib
import time
import numpy as np
from scipy.optimize import lsq_linear
from threadpoolctl import threadpool_limits

from .data import ROOT, INPUTS, IQ, get_profiles
from .experiment import condition,forward_fill,basic,aggregate,SCENARIOS

DT=10.0
NAMES=['G_c/C [1/s]','G_a/C [1/s]','k_I/C [K/(s A^2)]','k_n/C [K/(s rpm)]','k_n2/C [K/(s rpm^2)]']

def heat_features(x):
    return np.column_stack([x[:,5]**2+x[:,6]**2,np.abs(x[:,4]),x[:,4]**2])

def identify(data,ids,with_speed):
    xs,ds=[],[]
    for pid in ids:
        x,y=data[pid]
        pm=y[:,0].astype(float)
        h=heat_features(x.astype(float))
        mat=np.column_stack([x[:,1]-pm,x[:,0]-pm,h])[:-1]
        xs.append(mat if with_speed else mat[:,:3])
        ds.append(np.diff(pm)/DT)
    design=np.concatenate(xs)
    derivative=np.concatenate(ds)
    scales=np.linalg.norm(design,axis=0)
    assert np.all(scales>0)
    normalized=design/scales
    fit=lsq_linear(normalized,derivative,bounds=(0,np.inf),tol=1e-12,max_iter=1000)
    assert fit.success
    beta=fit.x/scales
    singular=np.linalg.svd(normalized,compute_uv=False)
    return beta,dict(coefficients=dict(zip(NAMES,beta.tolist())),
        training_transitions=len(design),normalized_design_rank=int(np.linalg.matrix_rank(normalized)),
        normalized_singular_values=singular.tolist(),normalized_condition_number=float(singular[0]/singular[-1]),
        derivative_rmse_k_per_s=float(np.sqrt(np.mean((design@beta-derivative)**2))),
        thermal_time_constant_s=float(1/beta[:2].sum()),
        caveat='Only ratios identifiable; absolute C, G, loss coefficients are scale-invariant and NOT identified.')

def predict(x,beta,initial=None):
    out=np.empty(len(x))
    out[0]=float(np.mean(x[0,:2])) if initial is None else initial
    gamma=float(beta[:2].sum())
    decay=np.exp(-DT*gamma)
    weight=-np.expm1(-DT*gamma)/gamma if gamma>1e-15 else DT
    forcing=x[:,1]*beta[0]+x[:,0]*beta[1]+heat_features(x)[:,:len(beta)-2]@beta[2:]
    for k in range(1,len(x)):
        out[k]=decay*out[k-1]+weight*forcing[k-1]
    return out

def main():
    frozen_path=ROOT/'reports/reference_full.json'
    original=frozen_path.read_bytes()
    frozen=json.loads(original)
    sets,data=get_profiles(20)
    assert frozen['split']==sets and frozen['dt']==DT
    train=np.concatenate([data[i][0] for i in sets['train']])
    median=np.median(train,axis=0)
    iq_sd=float(train[:,IQ].std())
    result=dict(protocol='effective_lptn_v1',split=sets,dt_seconds=DT,
        initialization='Mean of first measured ambient and coolant; no test target temperature.',
        fit='Training profiles only; nonnegative derivative least squares; exact ZOH inference.',
        frozen_experiment_sha256=hashlib.sha256(original).hexdigest(),models={})
    trace={}
    for name,speed in [('LPTN_I2',False),('LPTN_I2_speed',True)]:
        beta,diagnostics=identify(data,sets['train'],speed)
        def infer(pid,scenario):
            x,y=data[pid]
            seen,active=condition(x,pid,scenario,iq_sd)
            filled=forward_fill(seen,median).astype(float)
            start=time.perf_counter()
            pred=predict(filled,beta)
            latency=(time.perf_counter()-start)*1000/len(pred)
            assert np.isfinite(pred).all()
            return y[:,0],pred,active,latency
        cal=np.concatenate([np.abs(y-p) for pid in sets['calibration'] for y,p,*_ in [infer(pid,'clean')]])
        width=float(np.quantile(cal,.9,method='higher'))
        block=dict(**diagnostics,calibration_90_half_width_c=width,scenarios={})
        for scenario in SCENARIOS:
            rows={}
            for pid in sets['test']:
                y,p,active,latency=infer(pid,scenario)
                rows[str(pid)]=dict(**basic(y,p,active),coverage90=float(np.mean(np.abs(y-p)<=width)),cpu_ms_per_sample=latency)
                if scenario=='clean':
                    trace[f'{name}_{pid}']=np.column_stack([np.arange(len(y))*DT,y,p])
            total=sum(r['n'] for r in rows.values())
            block['scenarios'][scenario]=dict(**aggregate(list(rows.values())),profiles=rows,
                coverage90=sum(r['n']*r['coverage90'] for r in rows.values())/total,
                cpu_ms_per_sample_median=float(np.median([r['cpu_ms_per_sample'] for r in rows.values()])))
            print(name,scenario,{k:round(block['scenarios'][scenario][k],4) for k in ['mae','rmse','maxae','coverage90']},flush=True)
        result['models'][name]=block
    result['frozen_comparators']={n:m['scenarios'] for n,m in frozen['models'].items()}
    result['initial_temperature_sensitivity']=dict(profile=46,
        mean_boundary_initial_c=float(data[46][0][0,:2].mean()),
        true_initial_pm_c=float(data[46][1][0,0]),
        true_initial_used_in_inference=False)
    (ROOT/'results/lptn.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    np.savez_compressed(ROOT/'results/lptn-traces.npz',**trace)
    assert frozen_path.read_bytes()==original

if __name__=='__main__':
    with threadpool_limits(limits=1):
        main()
