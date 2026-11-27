"""Check nDCG and recall calculations against BEIR's official evaluator."""
from beir.retrieval.evaluation import EvaluateRetrieval
from src.evaluation import evaluate_run

def test_ndcg_and_recall_match_beir_evaluator():
    qrels={'q1':{'d1':1,'d2':0},'q2':{'d3':1}}
    run={'q1':['d2','d1'],'q2':['other']}
    ours,_=evaluate_run(run,qrels)
    beir_run={qid:{doc:float(100-rank) for rank,doc in enumerate(docs)} for qid,docs in run.items()}
    ndcg,_,recall,_=EvaluateRetrieval.evaluate(qrels,beir_run,[10,100])
    assert abs(ours['ndcg@10']-ndcg['NDCG@10'])<1e-5
    assert abs(ours['recall@10']-recall['Recall@10'])<1e-5
