from src.hybrid_retrieval import reciprocal_rank_fusion
from src.statistics import paired_bootstrap

def test_deterministic_repeats():
 ranks=[[('d2',1),('d1',.5)],[('d1',.2)]]
 assert reciprocal_rank_fusion(ranks)==reciprocal_rank_fusion(ranks)
 a=paired_bootstrap([1,2,3],[0,1,2],1000,123);b=paired_bootstrap([1,2,3],[0,1,2],1000,123)
 assert a==b and a['mean_difference']==1
