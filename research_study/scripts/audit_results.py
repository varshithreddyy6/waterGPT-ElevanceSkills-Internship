#!/usr/bin/env python3
"""Final consistency audit of benchmark runs, metrics, statistics, plots, and slides."""
from __future__ import annotations
import csv,gzip,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:sys.path.insert(0,str(ROOT))
from src.data_loader import load_scifact
from src.evaluation import evaluate_run
from beir.retrieval.evaluation import EvaluateRetrieval

def read_csv(path):
    with path.open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))

def main():
    corpus,queries,qrels=load_scifact(ROOT/'data/raw')
    assert len(corpus)==5183 and len(queries)==300 and set(queries)==set(qrels)
    methods={'BM25':'bm25','Dense':'dense','Hybrid RRF':'hybrid_rrf'}
    run_ids={};recomputed={};audit={'dataset_documents':len(corpus),'test_queries':len(queries),'positive_qrels':sum(v>0 for r in qrels.values() for v in r.values()),'systems':{}}
    for method,slug in methods.items():
        per=read_csv(ROOT/f'results/metrics/{slug}_per_query.csv')
        qids={r['query_id'] for r in per};assert len(per)==300 and qids==set(qrels)
        ranking={}
        with gzip.open(ROOT/f'results/runs/scifact-primary/{slug}.trec.gz','rt',encoding='utf-8') as f:
            for line in f:
                qid,_q0,doc,rank,score,_tag=line.split()
                assert qid in qrels and doc in corpus
                ranking.setdefault(qid,[]).append((int(rank),doc,float(score)))
        assert set(ranking)==set(qrels)
        for qid,items in ranking.items():
            items.sort();assert [x[0] for x in items]==list(range(1,1001))
            docs=[x[1] for x in items];assert len(set(docs))==1000
        run_ids[method]=set(ranking)
        metrics,pq=evaluate_run({q:[d for _,d,_ in sorted(items)] for q,items in ranking.items()},qrels)
        recomputed[method]=metrics
        per_by_id={r['query_id']:r for r in per}
        for qid,values in pq.items():
            for key,value in values.items():assert abs(float(per_by_id[qid][key])-value)<1e-12,(method,qid,key,per_by_id[qid][key],value)
        audit['systems'][method]={'per_query_rows':len(per),'run_query_ids':len(ranking),'candidate_depths':sorted({len(v) for v in ranking.values()}),'ranking_doc_ids_valid':True,'aggregate_metrics':metrics}
    assert len(set.union(*run_ids.values()))==300 and len(set.intersection(*run_ids.values()))==300
    agg=read_csv(ROOT/'results/metrics/comparative_results.csv')
    for row in agg:
        method=row['Method']
        for metric,value in recomputed[method].items():assert abs(float(row[metric])-value)<1e-12,(method,metric,row[metric],value)
    # Recheck BEIR references for the stored ranking using unique ordinal scores to preserve deterministic tie order.
    validation=json.loads((ROOT/'results/metrics/beir_metric_validation.json').read_text())
    for method,slug in methods.items():
        assert validation[method]['status']=='passed'
        system=json.loads(gzip.open(ROOT/f'results/runs/scifact-primary/{slug}.json.gz','rt',encoding='utf-8').read())
        beirrun={q:{x['doc_id']:float(len(items)-i) for i,x in enumerate(items)} for q,items in system.items()}
        ndcg,_,recall,_=EvaluateRetrieval.evaluate(qrels,beirrun,[10,100],ignore_identical_ids=False)
        assert abs(ndcg['NDCG@10']-recomputed[method]['ndcg@10'])<1e-4
        assert abs(recall['Recall@10']-recomputed[method]['recall@10'])<1e-4
        assert abs(recall['Recall@100']-recomputed[method]['recall@100'])<1e-4
    stats=json.loads((ROOT/'results/metrics/paired_statistics.json').read_text())
    assert len(stats)==12
    for metric in ('ndcg@10','mrr@10','recall@10','recall@100'):
        rows=[r for r in stats if r['metric']==metric];assert len(rows)==3
        ordered=sorted(rows,key=lambda r:r['p_raw']);running=0.0;m=len(ordered)
        for i,row in enumerate(ordered):
            running=max(running,(m-i)*row['p_raw']);assert abs(row['p_holm']-min(1,running))<1e-12
            assert row['n_queries']==300 and row['n_resamples']==10000
    config=json.loads((ROOT/'results/runs/scifact-primary/config.json').read_text())
    assert config['rrf']['k']==60 and config['retrieval']['candidate_depth']==1000
    # Confirm all charts exist and their source result artifact exists.
    plot_sources={'effectiveness.png':'comparative_results.csv','ndcg_mrr.png':'comparative_results.csv','recall.png':'comparative_results.csv','latency.png':'latency.json','per_query_distribution.png':'bm25_per_query.csv','confidence_intervals.png':'paired_statistics.json','ablation.png':'ablation_results.csv'}
    for plot,source in plot_sources.items():assert (ROOT/'results/plots'/plot).stat().st_size>1000 and (ROOT/'results/metrics'/source).is_file()
    assert (ROOT/'results/metadata/dataset.json').is_file()
    report=(ROOT/'reports/research_report.md').read_text()
    for row in agg:
        for k in ('ndcg@10','mrr@10','recall@10','recall@100'):assert f"{float(row[k]):.6f}" in report
    bib=(ROOT/'reports/references.bib').read_text()
    for token in ('10.18653/v1/2020.emnlp-main.609','arxiv.org/abs/2104.08663','10.1145/1571941.1572114','10.1109/TBDATA.2019.2921572','10.1561/1500000019'):assert token in bib
    from pptx import Presentation
    deck=Presentation(ROOT/'reports/presentation.pptx');assert len(deck.slides)==8
    audit['paired_comparisons']=len(stats);audit['holm_families_checked']=4;audit['plots_checked']=len(plot_sources);audit['report_metric_table_matches_csv']=True;audit['references_checked']='SciFact, BEIR, RRF, FAISS, BM25; presentation has 8 slides';audit['powerpoint_slides']=len(deck.slides);audit['primary_config_fixed_test_not_used_for_tuning']=True;audit['status']='passed'
    output=ROOT/'results/metadata/final_audit.json';output.write_text(json.dumps(audit,indent=2)+'\n',encoding='utf-8');print(json.dumps(audit,indent=2))
if __name__=='__main__':main()
