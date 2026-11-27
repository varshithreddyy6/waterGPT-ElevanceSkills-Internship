from src.lexical_retrieval import BM25Retriever

def test_bm25_order_and_empty():
 c={'b':{'title':'water quality','text':'river'},'a':{'title':'astronomy','text':'stars'},'c':{'title':'botany','text':'leaves'},'d':{'title':'history','text':'archives'}}
 r=BM25Retriever(c); assert r.search('water')[0][0]=='b'; assert r.search('  ')==[]
