from pathlib import Path
import hashlib
from itertools import combinations
import json
import zipfile
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
ZIP = ROOT / "data/kaggle-pmsm.zip"
INPUTS = ["ambient", "coolant", "u_d", "u_q", "motor_speed", "i_d", "i_q"]
TARGETS = ["pm", "stator_yoke", "stator_tooth", "stator_winding"]
IQ = INPUTS.index("i_q")
SEED = 260711
NATIVE_SECONDS = 0.5

def read_data():
    from .acquire import verify
    verify(ZIP)
    with zipfile.ZipFile(ZIP) as z, z.open("measures_v2.csv") as f:
        columns = f.readline().decode("utf-8-sig").strip().split(",")
        raw = np.loadtxt(f, dtype=np.float32, delimiter=",")
    assert set(INPUTS + TARGETS + ["profile_id"]).issubset(columns)
    return columns, raw

def split(ids):
    rng = np.random.default_rng(SEED)
    fixed = [60, 62, 74]
    assert set(fixed) <= set(ids)
    rem = rng.permutation(sorted(set(ids)-set(fixed))).tolist()
    return dict(test=sorted(fixed+rem[:5]), validation=sorted(rem[5:14]),
                calibration=sorted(rem[14:26]), train=sorted(rem[26:]))

def audit():
    (ROOT/'results').mkdir(exist_ok=True)
    columns, raw = read_data()
    ids, counts = np.unique(raw[:, columns.index("profile_id")].astype(int), return_counts=True)
    profiles = split(ids.tolist())
    assert len({v for part in profiles.values() for v in part}) == len(ids)
    meta = json.loads((ROOT/"data/kaggle-metadata.json").read_text(encoding="utf-8"))
    hasher = hashlib.sha256()
    with zipfile.ZipFile(ZIP) as z, z.open("measures_v2.csv") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(block)
    profile_col=raw[:,columns.index("profile_id")]
    edges=np.r_[0,np.flatnonzero(np.diff(profile_col))+1,len(raw)]
    same=np.diff(profile_col)==0
    checks={}
    for name in ["pm","ambient","coolant","motor_speed","i_q"]:
        c=raw[:,columns.index(name)]
        step=np.abs(np.diff(c))[same]
        q1,q3=np.quantile(c,[.25,.75])
        checks[name]=dict(tukey_flags=int(((c<q1-1.5*(q3-q1))|(c>q3+1.5*(q3-q1))).sum()),
                          within_profile_abs_step_p99=float(np.quantile(step,.99)),
                          within_profile_abs_step_max=float(step.max()))
    report = dict(version=meta["currentVersionNumber"], license=meta["licenseName"], updated=meta["lastUpdated"],
        archive_bytes=ZIP.stat().st_size, csv_sha256=hasher.hexdigest(), rows=len(raw), columns=columns,
        sampling_seconds=NATIVE_SECONDS, hours=len(raw)*NATIVE_SECONDS/3600,
        split=profiles, sample_counts={str(i):int(n) for i,n in zip(ids,counts)},
        split_rows={k:int(np.isin(profile_col,v).sum()) for k,v in profiles.items()},
        contiguous_blocks=len(edges)-1, repeated_profile_blocks=int(len(edges)-1-len(ids)),
        exact_duplicate_rows=int(len(raw)-len(np.unique(raw,axis=0))),
        anomaly_screen=checks,
        columns_stats={key:dict(nonfinite=int((~np.isfinite(c)).sum()),mean=float(np.nanmean(c)),std=float(np.nanstd(c)),
            quantiles=np.nanquantile(c,[0,.01,.5,.99,1]).tolist()) for key,c in zip(columns,raw.T)})
    path=ROOT/"results/data-audit.json"
    path.write_text(json.dumps(report,indent=2,allow_nan=False),encoding="utf-8")
    print(f"Audit: {len(raw):,} rows / {len(ids)} profiles, groups: "+str({k:len(v) for k,v in profiles.items()}),flush=True)
    return report

def get_profiles(stride):
    columns, raw = read_data()
    key=raw[:,columns.index("profile_id")].astype(int)
    sets=split(np.unique(key).tolist())
    assert all(not set(a).intersection(b) for a,b in combinations(sets.values(),2))
    assert sum(map(len,sets.values()))==len(np.unique(key))
    edges=np.r_[0,np.flatnonzero(np.diff(key))+1,len(key)]
    assert len(edges)-1==len(np.unique(key)), "Do not bridge disjoint blocks of a profile"
    xcols=[columns.index(n) for n in INPUTS]
    ycols=[columns.index(n) for n in TARGETS]
    data={int(key[a]):(raw[a:b:stride,xcols],raw[a:b:stride,ycols]) for a,b in zip(edges[:-1],edges[1:])}
    assert all(np.isfinite(x).all() and np.isfinite(y).all() for x,y in data.values())
    return sets,data

if __name__ == "__main__":
    audit()
