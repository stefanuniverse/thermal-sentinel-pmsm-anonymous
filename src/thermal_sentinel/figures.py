"""All-model/scenario evidence grid, not a plot of only favourable results.

Contract: quantitative grid; source=aggregate experiment metrics, deg C and
coverage. 183 mm report, editable SVG/PDF and 300dpi PNG. No smoothing,
significance claims, raw observations, or synthetic placeholder values.
"""
import argparse
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from .data import ROOT

LABELS={'Ridge':'Ridge + proxies','Ridge_plain':'Ridge raw','TNN':'TNN (10 epochs)',
    'TNN_signed_ablation':'TNN signed','TNN_reconstruct':'TNN reconstruction'}
plt.rcParams.update({'font.family':'sans-serif','font.sans-serif':['Arial','DejaVu Sans'],
    'font.size':7,'axes.spines.top':False,'axes.spines.right':False,'legend.frameon':False,
    'svg.fonttype':'none','pdf.fonttype':42})

def render(source,dest):
    result=json.loads(source.read_text(encoding='utf-8'))
    dest.mkdir(parents=True,exist_ok=True)
    cases=['clean','random_missing','outage','bias','drift','noise']
    colors=['#416983','#8eacb8','#c28248','#b6a89a','#647a66']
    fig,axes=plt.subplots(1,2,figsize=(7.205,3.65),layout='constrained')
    for (name,m),color in zip(result['models'].items(),colors):
        axes[0].plot(range(6),[m['scenarios'][c]['mae'] for c in cases],'-o',lw=1,ms=3,color=color,label=LABELS[name])
        axes[1].plot(range(6),[100*m['scenarios'][c]['coverage'][2] for c in cases],'-o',lw=1,ms=3,color=color)
    axes[0].set_ylabel('PM MAE (deg C)')
    axes[1].set_ylabel('Empirical 90% interval coverage (%)')
    axes[1].axhline(90,color='#999999',ls='--',lw=.7)
    for ax in axes:
        ax.set_xticks(range(6),['Clean','Missing','Outage','Bias','Drift','Noise'],rotation=35,ha='right')
        ax.grid(axis='y',color='#eeeeee',lw=.6)
    fig.legend(*axes[0].get_legend_handles_labels(),loc='outside lower center',ncols=3,fontsize=6)
    fig.suptitle('All five methods, all six conditions: accuracy is not robustness',fontsize=9)
    fig.savefig(dest/'robustness.svg',bbox_inches='tight')
    svg=dest/'robustness.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text(encoding='utf-8').splitlines())+'\n',encoding='utf-8')
    fig.savefig(dest/'robustness.pdf',bbox_inches='tight')
    fig.savefig(dest/'robustness.png',dpi=300,bbox_inches='tight')
    plt.close(fig)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--input',type=Path,default=ROOT/'reports/reference_full.json')
    ap.add_argument('--out',type=Path,default=ROOT/'results/figures')
    args=ap.parse_args();render(args.input,args.out)

if __name__=='__main__':main()
