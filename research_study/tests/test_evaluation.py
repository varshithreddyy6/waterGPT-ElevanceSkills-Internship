from src.evaluation import evaluate_query,per_query_metrics,aggregate_metrics

def test_known_metrics():
 m=evaluate_query(['d2','d1'],{'d1':1},2)
 assert m['mrr']==.5 and m['recall']==1 and m['ndcg']>0

def test_zero_judgment_query_included():
 pq=per_query_metrics({'q1':['d1'],'q2':[]},{'q1':{'d1':1},'q2':{}})
 assert pq['q2']['ndcg@10']==0 and aggregate_metrics(pq)['mrr@10']==.5

def test_relevance_missing_from_run_is_zero():
 assert evaluate_query([],{'d1':1},10)['recall']==0
