"""SentenceTransformer embeddings and exact cosine retrieval via FAISS IP."""
from __future__ import annotations
import hashlib, json, logging, time
from pathlib import Path
from typing import Any
import numpy as np
LOG=logging.getLogger(__name__)
DEFAULT_MODEL='sentence-transformers/all-MiniLM-L6-v2'

class DenseRetriever:
    """Exact cosine search by L2-normalized vectors and FAISS inner product."""
    def __init__(self, corpus: dict[str,dict[str,Any]], model_name: str=DEFAULT_MODEL, device: str|None=None, fields: str='title_abstract', batch_size: int=64, cache_dir: Path|None=None):
        if not corpus: raise ValueError('Corpus must not be empty')
        try:
            import faiss
            from sentence_transformers import SentenceTransformer
        except ImportError as exc: raise RuntimeError('Install research_study/requirements.txt to enable dense retrieval') from exc
        self.faiss=faiss; self.model_name=model_name; self.fields=fields; self.device=device
        self.ids=list(corpus); self.batch_size=batch_size
        texts=[(' '.join(x for x in (str(corpus[i].get('title') or '').strip(),str(corpus[i].get('text') or '').strip()) if x) if fields=='title_abstract' else str(corpus[i].get('title') or '').strip()) for i in self.ids]
        if fields not in ('title','title_abstract'): raise ValueError(f'Unsupported fields: {fields}')
        text_hash=hashlib.sha256('\n'.join(texts).encode('utf-8')).hexdigest()[:16]
        self.model_load_seconds=0.0; self.embedding_seconds=0.0; self.index_build_seconds=0.0; self.cache_hit=False
        cache_dir=Path(cache_dir) if cache_dir else None
        cache_path=cache_dir/f"{model_name.replace('/','_')}_{fields}_{len(self.ids)}_{text_hash}.npz" if cache_dir else None
        self.cache_path=cache_path
        started=time.perf_counter(); self.model=SentenceTransformer(model_name,device=device); self.model_load_seconds=time.perf_counter()-started
        self.actual_device=str(self.model.device); self.max_seq_length=int(self.model.max_seq_length)
        vectors=None
        if cache_path and cache_path.exists():
            cached=np.load(cache_path,allow_pickle=False)
            if list(cached['ids'].astype(str))==self.ids: vectors=cached['vectors'].astype('float32'); self.cache_hit=True
        if vectors is None:
            started=time.perf_counter(); vectors=self.model.encode(texts,batch_size=batch_size,show_progress_bar=False,convert_to_numpy=True,normalize_embeddings=True).astype('float32'); self.embedding_seconds=time.perf_counter()-started
            if cache_path:
                cache_path.parent.mkdir(parents=True,exist_ok=True); np.savez_compressed(cache_path,ids=np.asarray(self.ids),vectors=vectors)
                cache_path.with_suffix('.timing.json').write_text(json.dumps({'model_name':model_name,'fields':fields,'document_count':len(self.ids),'text_sha256':text_hash,'document_embedding_seconds':self.embedding_seconds},indent=2),encoding='utf-8')
        self.vectors=vectors
        started=time.perf_counter(); self.index=faiss.IndexFlatIP(vectors.shape[1]); self.index.add(vectors); self.index_build_seconds=time.perf_counter()-started
        self.dimension=int(vectors.shape[1]); LOG.info('Dense index ready: %d docs, dimension %d, model %s',len(self.ids),self.dimension,model_name)
    def search(self, query: str, top_k: int=1000) -> list[tuple[str,float]]:
        if not query.strip() or top_k<=0:return []
        q=self.model.encode([query],show_progress_bar=False,convert_to_numpy=True,normalize_embeddings=True).astype('float32')
        scores,indices=self.index.search(q,min(top_k,len(self.ids)))
        return [(self.ids[int(i)],float(s)) for s,i in zip(scores[0],indices[0]) if int(i)>=0]
    def search_timed(self, query: str, top_k: int=1000) -> tuple[list[tuple[str,float]],float,float]:
        start=time.perf_counter(); q=self.model.encode([query],show_progress_bar=False,convert_to_numpy=True,normalize_embeddings=True).astype('float32'); embed=time.perf_counter()-start
        start=time.perf_counter(); scores,indices=self.index.search(q,min(top_k,len(self.ids))); search=time.perf_counter()-start
        return [(self.ids[int(i)],float(s)) for s,i in zip(scores[0],indices[0]) if int(i)>=0],embed,search
    def save_index(self,path: Path) -> None:
        path=Path(path); path.parent.mkdir(parents=True,exist_ok=True); self.faiss.write_index(self.index,str(path)); path.with_suffix('.ids.json').write_text(json.dumps(self.ids),encoding='utf-8')
