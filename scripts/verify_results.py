"""Verify fresh run against every frozen scalar metric, excluding CPU timing."""
from pathlib import Path
import json
import math
import sys

ROOT=Path(__file__).resolve().parents[1]
reference=json.loads((ROOT/'reports/reference_full.json').read_text())
actual=json.loads((ROOT/'results/experiment.json').read_text())
errors=[];deltas=[];compared=0

def walk(a,b,path=''):
    global compared
    if 'cpu_ms' in path:return
    if isinstance(a,dict):
        for key,value in a.items():walk(value,b[key],path+'/'+key)
    elif isinstance(a,list):
        if len(a)!=len(b):errors.append(path+' length')
        for i,(x,y) in enumerate(zip(a,b)):walk(x,y,path+f'/{i}')
    elif isinstance(a,(int,float)) and not isinstance(a,bool):
        compared+=1
        deltas.append(abs(float(a)-float(b)))
        if not math.isclose(a,b,rel_tol=1e-5,abs_tol=1e-5):errors.append(path)
    elif a!=b:errors.append(path)

walk(reference,actual)
result=dict(passed=not errors,numeric_values_compared=compared,max_absolute_difference=max(deltas),
    errors=errors,rtol=1e-5,atol=1e-5,timing_excluded=True,
    acquisition='Existing official v3 ZIP reused via --source; both ZIP/CSV hashes checked. Fresh network ZIP download not exercised.',
    python_environment='New venv; include-system-site-packages=false; installed pinned dependencies and editable package.',
    models='All five methods retrained/evaluated; no original weights loaded.')
(ROOT/'reports/reproduction.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
print(json.dumps(result,indent=2))
sys.exit(0 if result['passed'] else 1)
