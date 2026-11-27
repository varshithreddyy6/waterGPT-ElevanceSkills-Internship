"""Reproducible, document-grounded retrieval disagreement examples."""
from __future__ import annotations
from typing import Any
from .evaluation import evaluate_query

def analyze_errors(runs: dict[str,dict[str,list[tuple[str,float]]]], queries: dict[str,dict], corpus: dict[str,dict], qrels: dict[str,dict[str,int]], limit: int=50) -> dict[str,Any]:
    """Select query winners by nDCG@10 and export real retrieved evidence with scores."""
    per_method={m:{q:[d for d,_ in ranking] for q,ranking in run.items()} for m,run in runs.items()}
    per_q={m:{q:evaluate_query(rank,qrels.get(q,{}),10)['ndcg'] for q,rank in rankings.items()} for m,rankings in per_method.items()}
    best=[]; all_fail=[]; disagreement=[]
    for qid,qdoc in queries.items():
        scores={m:per_q[m].get(qid,0.0) for m in runs}; max_score=max(scores.values(),default=0)
        winners=[m for m,v in scores.items() if v==max_score]
        if max_score==0: all_fail.append(qid)
        if len({tuple(per_method[m].get(qid,[])[:10]) for m in runs})>1:disagreement.append(qid)
        if len(winners)==1:best.append((qid,winners[0],scores))
    best.sort(key=lambda x:(-x[2][x[1]],x[0]))
    selected=set(q for q,_,_ in best[:limit]) | set(all_fail[:limit]) | set(disagreement[:limit])
    examples=[]
    for qid in sorted(selected):
        for method,run in runs.items():
            for rank,(docid,score) in enumerate(run.get(qid,[])[:10],1):
                doc=corpus.get(docid)
                if doc is None:raise ValueError(f'Retriever returned unknown document ID {docid}')
                examples.append({'query_id':qid,'query':queries[qid].get('text',''),'document_id':docid,'title':doc.get('title',''),'ground_truth_relevance':qrels.get(qid,{}).get(docid,0),'rank':rank,'score':float(score),'method':method,'query_ndcg@10':per_q[method].get(qid,0.0)})
    return {'queries_where_all_systems_fail':all_fail,'queries_with_rank_disagreement':disagreement,'unique_query_winners':[{'query_id':q,'method':m,'method_ndcg@10':s[m],'all_method_scores':s} for q,m,s in best],'retrieved_examples':examples}
