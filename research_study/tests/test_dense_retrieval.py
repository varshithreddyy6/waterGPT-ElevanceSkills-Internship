"""Dense adapter tests with synthetic vectors and no model download."""
import sys,types
import numpy as np
from src.dense_retrieval import DenseRetriever

class _FakeIndex:
    def __init__(self,dim):self.vectors=np.empty((0,dim),dtype='float32')
    def add(self,vectors):self.vectors=np.asarray(vectors,dtype='float32')
    def search(self,query,k):
        scores=np.asarray(query)@self.vectors.T
        order=np.argsort(-scores[0],kind='stable')[:k]
        return scores[:,order],order.reshape(1,-1)

class _FakeModel:
    device='cpu';max_seq_length=256
    def __init__(self,*args,**kwargs):pass
    def encode(self,texts,**kwargs):
        vectors=[]
        for text in texts:
            if text=='semantic query':vectors.append([0.0,1.0])
            elif 'doc one' in text:vectors.append([1.0,0.0])
            else:vectors.append([0.0,1.0])
        arr=np.asarray(vectors,dtype='float32')
        if kwargs.get('normalize_embeddings'):
            arr=arr/np.maximum(np.linalg.norm(arr,axis=1,keepdims=True),1e-12)
        return arr

def test_dense_ranking_and_empty_query_without_model_download(monkeypatch):
    faiss=types.SimpleNamespace(IndexFlatIP=_FakeIndex)
    st=types.ModuleType('sentence_transformers');st.SentenceTransformer=_FakeModel
    monkeypatch.setitem(sys.modules,'faiss',faiss);monkeypatch.setitem(sys.modules,'sentence_transformers',st)
    corpus={'d1':{'title':'doc one','text':'first'},'d2':{'title':'doc two','text':'second'}}
    retriever=DenseRetriever(corpus,cache_dir=None)
    results=retriever.search('semantic query',top_k=2)
    assert results[0][0]=='d2' and results[0][1]>results[1][1]
    assert retriever.dimension==2 and retriever.actual_device=='cpu'
    assert retriever.search(' ',10)==[]
