from src.hybrid_retrieval import reciprocal_rank_fusion

def test_rrf_and_deterministic_tie():
 a=[('b',100),('a',2)];b=[('a',.9),('b',.1)]
 result=reciprocal_rank_fusion([a,b],k=60)
 assert result[0][0]=='a' and abs(result[0][1]-result[1][1])<1e-12
 assert reciprocal_rank_fusion([a],60)==reciprocal_rank_fusion([a],60)

def test_rrf_deduplicates_within_ranked_list():
 assert reciprocal_rank_fusion([[('x',1),('x',2)]],60)==[('x',1/61)]
