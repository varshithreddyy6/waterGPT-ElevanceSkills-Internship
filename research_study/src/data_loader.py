"""SciFact dataset discovery, parsing, and integrity validation."""
from __future__ import annotations
import hashlib, json, logging
from pathlib import Path
from typing import Any
import pandas as pd

LOG = logging.getLogger(__name__)
REQUIRED = ("corpus.jsonl", "queries.jsonl", "qrels/test.tsv")

def sha256(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def find_dataset(root: Path) -> Path:
    """Find extracted SciFact folder under standard BEIR archive layouts."""
    root=Path(root)
    candidates=[root, root/'scifact', root/'scifact'/'scifact']
    for p in candidates:
        if all((p/x).is_file() for x in REQUIRED): return p
    for p in root.rglob('corpus.jsonl'):
        if all((p.parent/x).is_file() for x in REQUIRED): return p.parent
    raise FileNotFoundError(f"SciFact files not found below {root}. Run scripts/download_dataset.py")

def load_jsonl(path: Path) -> dict[str, dict[str, Any]]:
    rows={}
    with Path(path).open(encoding='utf-8') as f:
        for n,line in enumerate(f,1):
            if not line.strip(): continue
            obj=json.loads(line); key=str(obj.get('_id', obj.get('id','')))
            if not key: raise ValueError(f"Missing _id at {path}:{n}")
            if key in rows: raise ValueError(f"Duplicate identifier {key!r} in {path}")
            rows[key]=obj
    return rows

def load_qrels(path: Path) -> dict[str, dict[str,int]]:
    frame=pd.read_csv(path,sep='\t',dtype={'query-id':str,'corpus-id':str})
    expected={'query-id','corpus-id','score'}
    if not expected.issubset(frame.columns): raise ValueError(f"qrels columns missing: {expected-set(frame.columns)}")
    if frame.duplicated(['query-id','corpus-id']).any(): raise ValueError("Duplicate query/document qrels")
    qrels: dict[str,dict[str,int]]={}
    for q,d,s in frame[['query-id','corpus-id','score']].itertuples(index=False,name=None):
        qrels.setdefault(str(q),{})[str(d)]=int(s)
    return qrels

def load_scifact(root: Path) -> tuple[dict[str,dict],dict[str,dict],dict[str,dict[str,int]]]:
    folder=find_dataset(root)
    corpus=load_jsonl(folder/'corpus.jsonl'); queries=load_jsonl(folder/'queries.jsonl'); qrels=load_qrels(folder/'qrels/test.tsv')
    missing_q=set(qrels)-set(queries)
    missing_d={d for rels in qrels.values() for d in rels if d not in corpus}
    if missing_q: raise ValueError(f"qrels reference missing queries: {sorted(missing_q)[:5]}")
    if missing_d: raise ValueError(f"qrels reference missing documents: {sorted(missing_d)[:5]}")
    test_queries={qid:queries[qid] for qid in qrels}
    if len(corpus)<4000 or len(test_queries)<250 or not qrels: raise ValueError(f"Unexpected SciFact size: {len(corpus)} docs, {len(test_queries)} test queries, {len(qrels)} qrels")
    LOG.info('Loaded SciFact test split: %d documents, %d queries (%d total query records), %d judged queries',len(corpus),len(test_queries),len(queries),len(qrels))
    return corpus,test_queries,qrels

def validate_dataset(root: Path, metadata_path: Path|None=None) -> dict[str,Any]:
    folder=find_dataset(root); corpus,queries,qrels=load_scifact(folder)
    all_queries=load_jsonl(folder/'queries.jsonl')
    archive=Path(root)/'scifact.zip'
    archive_metadata={'md5':hashlib.md5(archive.read_bytes()).hexdigest(),'sha256':sha256(archive)} if archive.is_file() else None
    metadata={'dataset':'BEIR SciFact','dataset_version':archive_metadata['md5'] if archive_metadata else 'source files identified by SHA-256','source':'https://github.com/beir-cellar/beir','dataset_url':'https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/scifact.zip','archive_retrieval_policy':'The downloader prefers the official BEIR host and permits only an alternate mirror whose archive matches the published BEIR MD5.','split':'test','counts':{'documents':len(corpus),'queries_all_records':len(all_queries),'test_queries':len(queries),'qrel_queries':len(qrels),'qrels':sum(map(len,qrels.values())),'positive_qrels':sum(s>0 for r in qrels.values() for s in r.values())},'archive':archive_metadata,'sha256':{n:sha256(folder/n) for n in REQUIRED},'files':{n:str((folder/n).relative_to(Path(root))) for n in REQUIRED},'missing_qrel_queries':0,'missing_qrel_documents':0,'duplicate_document_ids':0}
    if metadata_path:
        metadata_path=Path(metadata_path)
        if metadata_path.exists():
            try:
                previous=json.loads(metadata_path.read_text(encoding='utf-8'))
                if previous.get('dataset_version')==metadata.get('dataset_version') and previous.get('archive',{}).get('sha256')==metadata.get('archive',{}).get('sha256') and previous.get('archive',{}).get('retrieval_source'):
                    metadata['archive']['retrieval_source']=previous['archive']['retrieval_source']
            except (OSError,json.JSONDecodeError,AttributeError):pass
        metadata_path.parent.mkdir(parents=True,exist_ok=True); metadata_path.write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
    return metadata
