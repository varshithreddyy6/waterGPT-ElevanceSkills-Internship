"""Latency summaries and controlled repeated query timing."""
from __future__ import annotations
import time
import numpy as np

def summarize_times(seconds: list[float]) -> dict[str,float]:
    if not seconds:return {'mean_seconds':0.0,'median_seconds':0.0,'p95_seconds':0.0,'n':0}
    a=np.asarray(seconds,dtype=float)
    return {'mean_seconds':float(a.mean()),'median_seconds':float(np.median(a)),'p95_seconds':float(np.quantile(a,.95)),'n':len(a)}

def benchmark_queries(search_fn, queries: list[str], top_k: int=1000, warmups: int=10, repeats: int=3) -> dict:
    if not queries:return {'warmups':warmups,'repeats':repeats,'queries':0,'overall':summarize_times([]),'per_query_seconds':[]}
    for q in queries[:warmups]:search_fn(q,top_k)
    samples=[]
    for _ in range(repeats):
        for q in queries:s=time.perf_counter(); search_fn(q,top_k); samples.append(time.perf_counter()-s)
    return {'warmups':min(warmups,len(queries)),'repeats':repeats,'queries':len(queries),'overall':summarize_times(samples),'per_query_seconds':samples}
