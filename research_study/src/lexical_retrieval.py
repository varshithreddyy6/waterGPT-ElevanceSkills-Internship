"""BM25Okapi lexical retrieval."""
from __future__ import annotations
import time
from typing import Any
from rank_bm25 import BM25Okapi
from .preprocessing import document_text, tokenize

class BM25Retriever:
    """Deterministic BM25 with title+abstract by default."""
    def __init__(self, corpus: dict[str,dict[str,Any]], k1: float=1.5, b: float=0.75, fields: str='title_abstract'):
        if not corpus: raise ValueError('Corpus must not be empty')
        self.ids=list(corpus); self.fields=fields
        self.tokenized=[tokenize(document_text(corpus[i],fields)) for i in self.ids]
        self.index=BM25Okapi(self.tokenized,k1=k1,b=b)
    def search(self, query: str, top_k: int=1000) -> list[tuple[str,float]]:
        if top_k<0: raise ValueError('top_k must be nonnegative')
        tokens=tokenize(query)
        if not tokens or top_k==0: return []
        scores=self.index.get_scores(tokens)
        order=sorted(range(len(self.ids)),key=lambda i:(-float(scores[i]),self.ids[i]))[:top_k]
        return [(self.ids[i],float(scores[i])) for i in order]
    def timed_search(self, query: str, top_k: int=1000) -> tuple[list[tuple[str,float]],float]:
        start=time.perf_counter(); result=self.search(query,top_k); return result,time.perf_counter()-start
