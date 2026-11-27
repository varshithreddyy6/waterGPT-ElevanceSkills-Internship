"""Reciprocal Rank Fusion over ranked lexical and semantic results."""
from __future__ import annotations
from collections.abc import Sequence

def reciprocal_rank_fusion(rankings: Sequence[Sequence[tuple[str,float]]], k: int=60, top_k: int|None=None) -> list[tuple[str,float]]:
    """Fuse ranked lists; ranks are one-based, ties break lexicographically."""
    if k<=0: raise ValueError('RRF k must be positive')
    scores: dict[str,float]={}
    for ranking in rankings:
        seen=set()
        for rank,(doc_id,_score) in enumerate(ranking,1):
            if doc_id in seen: continue
            seen.add(doc_id); scores[doc_id]=scores.get(doc_id,0.0)+1.0/(k+rank)
    ordered=sorted(scores.items(),key=lambda x:(-x[1],x[0]))
    return ordered[:top_k] if top_k is not None else ordered
