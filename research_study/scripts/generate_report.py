#!/usr/bin/env python3
"""Generate publication-style plots from measured CSV/JSON outputs only."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np,pandas as pd

def main():
 root=ROOT;metrics=root/'results/metrics';plots=root/'results/plots';plots.mkdir(parents=True,exist_ok=True)
 file=metrics/'comparative_results.csv'
 if not file.exists():raise SystemExit('Run scripts/run_experiments.py before plotting.')
 df=pd.read_csv(file);methods=df['Method'].tolist();palette=['#4169E1','#E07A2D','#278A69']
 def grouped(cols,title,ylabel,name):
  x=np.arange(len(cols));w=.8/len(methods);fig,ax=plt.subplots(figsize=(8,4.8))
  for i,m in enumerate(methods):ax.bar(x+(i-(len(methods)-1)/2)*w,[df.loc[df.Method==m,c].iloc[0] for c in cols],w,label=m,color=palette[i%3])
  ax.set_xticks(x,cols);ax.set_ylabel(ylabel);ax.set_title(title);ax.legend(frameon=False);ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(plots/name,dpi=220);plt.close(fig)
 grouped(['ndcg@10','mrr@10','recall@10','recall@100'],'Retrieval effectiveness comparison','Macro-averaged score','effectiveness.png')
 grouped(['ndcg@10','mrr@10'],'Top-rank quality','Macro-averaged score','ndcg_mrr.png')
 grouped(['recall@10','recall@100'],'Retrieval coverage','Macro-averaged recall','recall.png')
 lat=metrics/'latency.json'
 if lat.exists():
  d=json.loads(lat.read_text())['steady_state'];fig,ax=plt.subplots(figsize=(7,4.5));x=np.arange(len(methods));width=.24
  for i,(stat,label) in enumerate((('mean_seconds','Mean'),('median_seconds','Median'),('p95_seconds','p95'))):ax.bar(x+(i-1)*width,[d[m][stat]*1000 for m in methods],width,label=label,color=palette[i])
  ax.set_xticks(x,methods);ax.set_ylabel('Single-query latency (ms)');ax.set_title('Steady-state retrieval latency');ax.legend(frameon=False);ax.grid(axis='y',alpha=.2);fig.tight_layout();fig.savefig(plots/'latency.png',dpi=220);plt.close(fig)
 for m in methods:
  path=metrics/f"{m.lower().replace(' ','_')}_per_query.csv"
  if path.exists():plt.hist(pd.read_csv(path)['ndcg@10'],bins=np.linspace(0,1,21),alpha=.5,label=m)
 if any((metrics/f"{m.lower().replace(' ','_')}_per_query.csv").exists() for m in methods):
  plt.xlabel('Per-query nDCG@10');plt.ylabel('Number of queries');plt.title('Per-query retrieval quality distribution');plt.legend(frameon=False);plt.tight_layout();plt.savefig(plots/'per_query_distribution.png',dpi=220);plt.close()
 stats=metrics/'paired_statistics.json'
 if stats.exists():
  rows=json.loads(stats.read_text());fig,axes=plt.subplots(2,2,figsize=(10,7));
  for ax,metric in zip(axes.flat,['ndcg@10','mrr@10','recall@10','recall@100']):
   pairs=[r for r in rows if r['metric']==metric];labels=[r['method_a']+' − '+r['method_b'] for r in pairs];means=[r['mean_difference'] for r in pairs];lo=[r['mean_difference']-r['ci_low'] for r in pairs];hi=[r['ci_high']-r['mean_difference'] for r in pairs];ax.errorbar(means,range(len(pairs)),xerr=[lo,hi],fmt='o',capsize=3,color='#284B63');ax.axvline(0,color='black',lw=.8);ax.set_yticks(range(len(pairs)),labels,fontsize=8);ax.set_title(metric);ax.grid(axis='x',alpha=.2)
  fig.suptitle('Paired query-level mean differences (95% bootstrap CI)');fig.tight_layout();fig.savefig(plots/'confidence_intervals.png',dpi=220);plt.close(fig)
 abl=metrics/'ablation_results.csv'
 if abl.exists():
  data=pd.read_csv(abl);fig,axes=plt.subplots(1,3,figsize=(14,4.5))
  for fields,g in data[data.ablation=='rrf_k'].groupby('fields'):axes[0].plot(g.value,g['ndcg@10'],marker='o',label=fields)
  axes[0].set_xlabel('RRF rank constant k');axes[0].set_ylabel('nDCG@10');axes[0].set_title('RRF k sensitivity');axes[0].legend(fontsize=8,frameon=False)
  for fields,g in data[data.ablation=='candidate_depth'].groupby('fields'):axes[1].plot(g.value,g['ndcg@10'],marker='o',label=fields)
  axes[1].set_xlabel('Component candidate depth');axes[1].set_ylabel('nDCG@10');axes[1].set_title('Candidate-depth sensitivity');axes[1].legend(fontsize=8,frameon=False)
  for i,fields in enumerate(('title','title_abstract')):
   g=data[(data.fields==fields)&(((data.ablation=='text_fields')&(data.value.isin(['BM25','Dense'])))|((data.ablation=='rrf_k')&(data.value.astype(str)=='60')))]
   lookup={}
   for _,row in g.iterrows():
    name=str(row['value']) if row['ablation']=='text_fields' else 'Hybrid RRF'
    lookup[name]=row['ndcg@10']
   order=['BM25','Dense','Hybrid RRF']
   for j,name in enumerate(order):axes[2].bar(j+(i-.5)*.35,lookup.get(name,0),.35,label=fields if j==0 else None,color=('#8B5CF6' if fields=='title' else '#1D8A72'))
  axes[2].set_xticks(range(3),['BM25','Dense','Hybrid']);axes[2].set_ylabel('nDCG@10');axes[2].set_title('Document-field ablation');axes[2].legend(fontsize=8,frameon=False)
  for ax in axes:ax.grid(axis='y',alpha=.2)
  fig.suptitle('Held-out descriptive ablations (not parameter tuning)');fig.tight_layout();fig.savefig(plots/'ablation.png',dpi=220);plt.close(fig)
 print(f'Plots generated in {plots}')
if __name__=='__main__':main()
