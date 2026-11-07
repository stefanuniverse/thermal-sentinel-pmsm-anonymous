"""Export all methods/scenarios, never select only favourable results."""
import argparse
import csv
import json
from pathlib import Path
from .data import ROOT

def sanitized(result):
    result=json.loads(json.dumps(result))
    for model in result['models'].values():
        for block in model['scenarios'].values():
            for row in block['profiles'].values():
                for field in ['worst_sample','worst_measured','worst_predicted']:
                    row.pop(field,None)
    return result

def export(source,dest,reference=False):
    result=json.loads(source.read_text(encoding='utf-8'))
    dest.mkdir(parents=True,exist_ok=True)
    result=sanitized(result)
    if reference:
        (dest/'reference_full.json').write_text(json.dumps(result,indent=2,allow_nan=False),encoding='utf-8')
    keys=['model','scenario','mae_c','rmse_c','maxae_c','macro_mae_c','coverage90','interval_width_c','fault_window_mae_c','hot_mae_c']
    rows=[];profiles=[]
    for name,model in result['models'].items():
        for case,m in model['scenarios'].items():
            rows.append([name,case,m['mae'],m['rmse'],m['maxae'],m['macro_mae'],m['coverage'][2],m['interval_width_c'],m['active']['mae'],m['hot']['mae']])
            for pid,p in m['profiles'].items():
                profiles.append([name,case,pid,p['n'],p['mae'],p['rmse'],p['maxae'],p['coverage'][2],p['active']['n'],p['active']['mae']])
    for path,fields,values in [(dest/'metrics.csv',keys,rows),(dest/'profile_metrics.csv',
        ['model','scenario','profile_id','n','mae_c','rmse_c','maxae_c','coverage90','fault_n','fault_mae_c'],profiles)]:
        with path.open('w',newline='',encoding='utf-8') as f:
            w=csv.writer(f);w.writerow(fields);w.writerows(values)
    print(f'Exported {len(rows)} method/scenario rows and {len(profiles)} profile rows. No raw sequences exported.')

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,default=ROOT/'results/experiment.json')
    ap.add_argument('--out',type=Path,default=ROOT/'results/export')
    ap.add_argument('--reference',action='store_true',help='Include sanitized scalar reference JSON; no time-series data')
    args=ap.parse_args();export(args.input,args.out,args.reference)

if __name__=='__main__':main()
