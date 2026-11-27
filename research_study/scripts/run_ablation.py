#!/usr/bin/env python3
"""Held-out test ablations; parameters are descriptive, not test-tuned."""
from __future__ import annotations
import argparse,json,time
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
import pandas as pd,yaml
from src.data_loader import load_scifact
from src.lexical_retrieval import BM25Retriever
from src.dense_retrieval import DenseRetriever
from src.hybrid_retrieval import reciprocal_rank_fusion
from src.evaluation import evaluate_run

def main():
 here=Path(__file__).resolve().parents[1]; p=argparse.ArgumentParser();p.add_argument('--data-dir',type=Path,default=here/'data/raw');p.add_argument('--device',default=None);a=p.parse_args();cfg=yaml.safe_load((here/'configs/default.yaml').read_text());corpus,queries,qrels=load_scifact(a.data_dir);depth=cfg['retrieval']['candidate_depth']; rows=[]
 dense_cache={}
 for fields in ('title_abstract','title'):
  bm=BM25Retriever(corpus,cfg['bm25']['k1'],cfg['bm25']['b'],fields)
  dense=DenseRetriever(corpus,cfg['dense']['model_name'],a.device or cfg['dense'].get('device'),fields,cfg['dense']['batch_size'],here/'data/cache')
  b_run={};d_run={}
  for qid,obj in queries.items():b_run[qid]=bm.search(obj.get('text',''),depth);d_run[qid]=dense.search(obj.get('text',''),depth)
  for k in (20,60,100):
   h={q:reciprocal_rank_fusion([b_run[q],d_run[q]],k,depth) for q in queries}
   metrics,_=evaluate_run({q:[d for d,_ in r] for q,r in h.items()},qrels)
   rows.append({'ablation':'rrf_k','value':k,'fields':fields,**metrics})
  for candidate_depth in (100,500,1000):
   h={q:reciprocal_rank_fusion([b_run[q][:candidate_depth],d_run[q][:candidate_depth]],60,candidate_depth) for q in queries}
   metrics,_=evaluate_run({q:[d for d,_ in r] for q,r in h.items()},qrels)
   rows.append({'ablation':'candidate_depth','value':candidate_depth,'fields':fields,**metrics})
  for name,run in [('BM25',b_run),('Dense',d_run)]:
   metrics,_=evaluate_run({q:[d for d,_ in r] for q,r in run.items()},qrels);rows.append({'ablation':'text_fields','value':name,'fields':fields,**metrics})
 out=here/'results/metrics/ablation_results.csv';pd.DataFrame(rows).to_csv(out,index=False);print(pd.DataFrame(rows).to_string(index=False))
if __name__=='__main__':main()
