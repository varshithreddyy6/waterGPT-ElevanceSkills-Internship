#!/usr/bin/env python3
"""Execute controlled BM25, dense, and RRF experiments on SciFact test."""
from __future__ import annotations
import argparse,csv,gzip,json,logging,os,platform,sys,time
from importlib.metadata import PackageNotFoundError,version
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path: sys.path.insert(0, str(ROOT))
import numpy as np, pandas as pd, yaml
from src.data_loader import load_scifact,validate_dataset
from src.preprocessing import document_text
from src.lexical_retrieval import BM25Retriever
from src.dense_retrieval import DenseRetriever
from src.hybrid_retrieval import reciprocal_rank_fusion
from src.evaluation import evaluate_run
from src.statistics import paired_comparisons
from src.error_analysis import analyze_errors
from src.latency import summarize_times

def dump_json(path,obj):
 path.parent.mkdir(parents=True,exist_ok=True); path.write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n',encoding='utf-8')
def run():
 here=Path(__file__).resolve().parents[1]
 p=argparse.ArgumentParser(); p.add_argument('--config',type=Path,default=here/'configs/default.yaml'); p.add_argument('--data-dir',type=Path,default=here/'data/raw'); p.add_argument('--run-id',default='scifact-primary'); p.add_argument('--device',default=None); a=p.parse_args()
 cfg=yaml.safe_load(a.config.read_text()); logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s'); log=logging.getLogger('experiment')
 corpus,queries,qrels=load_scifact(a.data_dir); validate_dataset(a.data_dir,here/'results/metadata/dataset.json')
 depth=int(cfg['retrieval']['candidate_depth']); fields=cfg['retrieval']['document_fields']; model=cfg['dense']['model_name']
 build={}; t=time.perf_counter(); bm=BM25Retriever(corpus,cfg['bm25']['k1'],cfg['bm25']['b'],fields); build['bm25_index_build_seconds']=time.perf_counter()-t
 dense=DenseRetriever(corpus,model,a.device or cfg['dense'].get('device'),fields,int(cfg['dense']['batch_size']),here/'data/cache')
 cold_embedding_seconds=dense.embedding_seconds
 if dense.cache_hit and dense.cache_path and dense.cache_path.with_suffix('.timing.json').exists():cold_embedding_seconds=json.loads(dense.cache_path.with_suffix('.timing.json').read_text())['document_embedding_seconds']
 build.update({'dense_model_load_seconds':dense.model_load_seconds,'document_embedding_seconds_this_run':dense.embedding_seconds,'document_embedding_cold_seconds':cold_embedding_seconds,'embedding_cache_hit':dense.cache_hit,'faiss_index_build_seconds':dense.index_build_seconds,'embedding_dimension':dense.dimension,'model_max_sequence_length':dense.max_seq_length,'device':dense.actual_device})
 method_runs={m:{} for m in ('BM25','Dense','Hybrid RRF')}; timings={m:[] for m in method_runs}; dense_encode=[]; faiss_times=[]; fusion_times=[]
 for idx,(qid,qobj) in enumerate(queries.items(),1):
  query=str(qobj.get('text',''))
  bm_res,bm_t=bm.timed_search(query,depth); de_res,de_emb,de_search=dense.search_timed(query,depth)
  t=time.perf_counter(); hy_res=reciprocal_rank_fusion([bm_res,de_res],cfg['rrf']['k'],depth); fuse=time.perf_counter()-t
  for m,r in [('BM25',bm_res),('Dense',de_res),('Hybrid RRF',hy_res)]:method_runs[m][qid]=r
  timings['BM25'].append(bm_t); timings['Dense'].append(de_emb+de_search); timings['Hybrid RRF'].append(bm_t+de_emb+de_search+fuse)
  dense_encode.append(de_emb); faiss_times.append(de_search); fusion_times.append(fuse)
  if idx%50==0:log.info('Retrieved %d/%d queries',idx,len(queries))
 # Warmups followed by repeated per-query measurements; separate from initial run collection.
 latency={}
 for method in method_runs:
  samples=[]
  for rep in range(int(cfg['latency']['repeats'])):
   for qid,qobj in list(queries.items())[:int(cfg['latency']['warmup_queries'])]:
    q=str(qobj.get('text','')); bm.search(q,depth); dense.search(q,depth); reciprocal_rank_fusion([bm.search(q,depth),dense.search(q,depth)],cfg['rrf']['k'],depth)
   for qid,qobj in queries.items():
    q=str(qobj.get('text','')); start=time.perf_counter()
    if method=='BM25':bm.search(q,depth)
    elif method=='Dense':dense.search(q,depth)
    else:reciprocal_rank_fusion([bm.search(q,depth),dense.search(q,depth)],cfg['rrf']['k'],depth)
    samples.append(time.perf_counter()-start)
  latency[method]=summarize_times(samples)
 # Initial per-query timings for execution-stage decomposition, plus repeated steady-state timings.
 latency['components']={'bm25_query':summarize_times(timings['BM25']),'dense_query_embedding':summarize_times(dense_encode),'faiss_search':summarize_times(faiss_times),'rrf_fusion':summarize_times(fusion_times),'hybrid_component_sum':summarize_times(timings['Hybrid RRF'])}
 summary={}; per_query={}
 for method,run in method_runs.items():
  summary[method],per_query[method]=evaluate_run({q:[d for d,_ in r] for q,r in run.items()},qrels)
 # Validate full-benchmark nDCG/recall against BEIR's official evaluation implementation.
 from beir.retrieval.evaluation import EvaluateRetrieval
 beir_validation={}
 for method,run in method_runs.items():
  # Use strictly descending ordinal scores so BEIR preserves our precomputed deterministic tie order.
  beir_run={q:{doc:float(len(ranks)-rank) for rank,(doc,_score) in enumerate(ranks)} for q,ranks in run.items()}
  beir_ndcg,_,beir_recall,_=EvaluateRetrieval.evaluate(qrels,beir_run,[10,100],ignore_identical_ids=False)
  check={'ndcg@10':float(beir_ndcg['NDCG@10']),'recall@10':float(beir_recall['Recall@10']),'recall@100':float(beir_recall['Recall@100'])}
  for key,reference in check.items():
   if abs(summary[method][key]-reference)>1e-4:raise AssertionError(f'BEIR metric mismatch for {method} {key}: local={summary[method][key]} BEIR={reference}')
  beir_validation[method]={'local_macro_metrics':summary[method],'beir_reference':check,'absolute_tolerance':1e-4,'score_mapping':'strictly descending ordinal scores preserve the saved deterministic ranking order, including tie-breaks','status':'passed'}
 out=here/'results'; run_dir=out/'runs'/a.run_id; run_dir.mkdir(parents=True,exist_ok=True)
 # TREC-style runfiles with explicit 1-based ranks and system scores.
 for method,run in method_runs.items():
  slug=method.lower().replace(' ','_');
  with gzip.open(run_dir/f'{slug}.trec.gz','wt',encoding='utf-8',compresslevel=6) as f:
   for qid,items in run.items():
    for rank,(doc,score) in enumerate(items,1):f.write(f'{qid} Q0 {doc} {rank} {score:.12g} {slug}\n')
  with gzip.open(run_dir/f'{slug}.json.gz','wt',encoding='utf-8',compresslevel=6) as f:
   json.dump({q:[{'doc_id':d,'score':s} for d,s in ranks] for q,ranks in run.items()},f,ensure_ascii=False,separators=(',',':'))
  pd.DataFrame([{'query_id':q,**metrics} for q,metrics in per_query[method].items()]).to_csv(out/'metrics'/f'{slug}_per_query.csv',index=False)
 pd.DataFrame([{'Method':m,**summary[m]} for m in method_runs]).to_csv(out/'metrics/comparative_results.csv',index=False)
 dump_json(out/'metrics/beir_metric_validation.json',beir_validation)
 stats=[]
 for metric in ('ndcg@10','mrr@10','recall@10','recall@100'):
  stats.extend(paired_comparisons(per_query,metric,int(cfg['statistics']['seed']),int(cfg['statistics']['bootstrap_resamples'])))
 dump_json(out/'metrics/paired_statistics.json',stats)
 dump_json(out/'metrics/latency.json',{'retrieval_depth':depth,'measurement':'single-query, repeated, CPU/GPU device in run metadata','steady_state':latency,'build_and_query_components_seconds':build})
 err=analyze_errors(method_runs,queries,corpus,qrels,int(cfg['error_analysis']['example_limit']))
 dump_json(out/'error_analysis/error_analysis.json',err)
 dump_json(run_dir/'config.json',cfg)
 packages={}
 for package in ('rank-bm25','sentence-transformers','faiss-cpu','beir','numpy','pandas','scipy','scikit-learn','torch','matplotlib'):
  try:packages[package]=version(package)
  except PackageNotFoundError:packages[package]='not-installed'
 try:
  import torch
  gpu={'available':torch.cuda.is_available(),'device_name':torch.cuda.get_device_name(0) if torch.cuda.is_available() else None}
 except Exception:gpu={'available':False,'device_name':None}
 try:memory_bytes=os.sysconf('SC_PAGE_SIZE')*os.sysconf('SC_PHYS_PAGES')
 except (ValueError,OSError,AttributeError):memory_bytes=None
 metadata={'run_id':a.run_id,'dataset':'BEIR SciFact','split':'test','query_count':len(queries),'corpus_count':len(corpus),'model':model,'embedding_dimension':dense.dimension,'model_max_sequence_length':dense.max_seq_length,'model_truncation':'Inputs exceeding the loaded SentenceTransformer max_seq_length are truncated by the model tokenizer.','candidate_depth':depth,'document_fields':fields,'rrf_k':cfg['rrf']['k'],'python':sys.version,'platform':platform.platform(),'processor':platform.processor(),'cpu_count':os.cpu_count(),'memory_bytes':memory_bytes,'gpu':gpu,'numpy':np.__version__,'pandas':pd.__version__,'packages':packages,'device':dense.actual_device,'timing_note':'Single-query retrieval; model and document index builds timed separately. Query latency includes component query embedding and ranking; hybrid includes both ranked lists and fusion. Warm-ups are not counted in steady-state summary.'}
 dump_json(out/'metadata'/f'{a.run_id}.json',metadata)
 logging.info('Results: %s',summary); print(pd.DataFrame([{'Method':m,**summary[m]} for m in method_runs]).to_string(index=False)); return 0
if __name__=='__main__':raise SystemExit(run())
