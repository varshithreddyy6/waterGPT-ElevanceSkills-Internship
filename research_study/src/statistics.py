"""Paired bootstrap and corrected paired tests for query-level outcomes."""
from __future__ import annotations
import numpy as np
from scipy.stats import wilcoxon

def paired_bootstrap(a, b, n_resamples: int=10000, seed: int=2026, confidence: float=.95) -> dict:
    """Bootstrap mean(a-b) paired by query; percentile interval, fixed RNG seed."""
    x=np.asarray(a,dtype=float); y=np.asarray(b,dtype=float)
    if x.shape!=y.shape or x.ndim!=1 or len(x)==0: raise ValueError('Paired arrays must be nonempty and have identical shape')
    dif=x-y; rng=np.random.default_rng(seed); means=np.empty(n_resamples)
    for start in range(0,n_resamples,500):
        size=min(500,n_resamples-start); idx=rng.integers(0,len(dif),size=(size,len(dif))); means[start:start+size]=dif[idx].mean(axis=1)
    alpha=1-confidence
    return {'mean_difference':float(dif.mean()),'ci_low':float(np.quantile(means,alpha/2)),'ci_high':float(np.quantile(means,1-alpha/2)),'confidence':confidence,'n_resamples':n_resamples,'seed':seed,'n_queries':len(dif)}

def paired_comparisons(per_query: dict[str,dict[str,dict[str,float]]], metric: str='ndcg@10', seed: int=2026, n_resamples: int=10000) -> list[dict]:
    """Compare all method pairs using paired bootstrap and Holm-corrected Wilcoxon."""
    from itertools import combinations
    methods=list(per_query); qids=sorted(set.intersection(*(set(per_query[m]) for m in methods)))
    rows=[]
    for left,right in combinations(methods,2):
        a=np.array([per_query[left][q][metric] for q in qids]); b=np.array([per_query[right][q][metric] for q in qids])
        boot=paired_bootstrap(a,b,n_resamples,seed)
        try: p=float(wilcoxon(a,b,zero_method='wilcox',alternative='two-sided').pvalue) if np.any(a!=b) else 1.0
        except ValueError: p=1.0
        rows.append({'method_a':left,'method_b':right,'metric':metric,'test':'two-sided paired Wilcoxon','p_raw':p,**boot})
    # Holm step-down familywise adjustment.
    order=sorted(range(len(rows)),key=lambda i:rows[i]['p_raw']); running=0.0; m=len(rows)
    for rank,i in enumerate(order):
        adjusted=min(1.0,max(running,(m-rank)*rows[i]['p_raw'])); rows[i]['p_holm']=adjusted; running=adjusted
    return rows
