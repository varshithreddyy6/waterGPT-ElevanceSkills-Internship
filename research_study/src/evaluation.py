"""BEIR-compatible nDCG, MRR, and recall with macro query averaging."""
from __future__ import annotations
import math
from collections.abc import Mapping, Sequence
import numpy as np
METRICS=('ndcg@10','mrr@10','recall@10','recall@100')

def evaluate_query(ranking: Sequence[str], relevant: Mapping[str,int], k: int=10) -> dict[str,float]:
    """Compute standard graded nDCG@k, reciprocal rank, and binary recall."""
    positives={d:int(g) for d,g in relevant.items() if int(g)>0}
    if not positives:return {'ndcg':0.0,'mrr':0.0,'recall':0.0}
    top=list(ranking[:k]); gains=[max(0,int(positives.get(d,0))) for d in top]
    dcg=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(gains))
    ideal=sorted(positives.values(),reverse=True)[:k]
    idcg=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(ideal))
    first=next((i+1 for i,d in enumerate(top) if d in positives),None)
    recall=len({d for d in top if d in positives})/len(positives)
    return {'ndcg':dcg/idcg if idcg else 0.0,'mrr':1.0/first if first else 0.0,'recall':recall}

def per_query_metrics(run: Mapping[str,Sequence[str]], qrels: Mapping[str,Mapping[str,int]]) -> dict[str,dict[str,float]]:
    """Return test-query metrics; queries without positive judgments score zero."""
    result={}
    for qid,rel in qrels.items():
        ranking=run.get(qid,())
        at10=evaluate_query(ranking,rel,10); at100=evaluate_query(ranking,rel,100)
        result[qid]={'ndcg@10':at10['ndcg'],'mrr@10':at10['mrr'],'recall@10':at10['recall'],'recall@100':at100['recall']}
    return result

def aggregate_metrics(per_query: Mapping[str,Mapping[str,float]]) -> dict[str,float]:
    """Macro average over all judged qrel query IDs, including zero-positive queries."""
    if not per_query:return {m:0.0 for m in METRICS}
    return {m:float(np.mean([float(row.get(m,0.0)) for row in per_query.values()])) for m in METRICS}

def evaluate_run(run: Mapping[str,Sequence[str]], qrels: Mapping[str,Mapping[str,int]]) -> tuple[dict[str,float],dict[str,dict[str,float]]]:
    pq=per_query_metrics(run,qrels); return aggregate_metrics(pq),pq
