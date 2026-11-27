# Evaluating Lexical, Dense, and Hybrid Retrieval Methods for Scientific Literature Search
## Interview presentation · BEIR SciFact results

### Slide 1 — Research problem
Scientific evidence retrieval faces vocabulary mismatch, exact scientific terminology, and competing latency/effectiveness goals. **Question:** Does combining lexical retrieval and semantic dense retrieval improve scientific literature discovery? We treat this as an empirical question, not an assumption.

### Slide 2 — Dataset and scope
Official BEIR SciFact test: **5,183 documents, 300 test queries, 339 positive judgments**. SciFact is claim-to-evidence retrieval over scientific abstracts—not an arXiv-only benchmark and not representative of every scientific discipline. All methods use the same official test qrels and IDs.

### Slide 3 — Controlled systems
- **BM25:** `rank_bm25.BM25Okapi`, k1=1.5, b=.75.
- **Dense:** `sentence-transformers/all-MiniLM-L6-v2`, 384 dimensions; normalized vectors and exact cosine via FAISS `IndexFlatIP`.
- Shared title + abstract/text; top-1,000 component candidates; CPU measurements; no paid APIs or benchmark tuning.

### Slide 4 — Hybrid fusion and evaluation
RRF score = sum `1/(60 + rank)` over BM25 and dense ranked lists; rank-based fusion, not raw-score blending. Macro nDCG@10, MRR@10, Recall@10, Recall@100; 10,000 paired bootstrap resamples and paired Wilcoxon with Holm correction. See `results/plots/effectiveness.png` and `results/plots/confidence_intervals.png`.

### Slide 5 — Measured retrieval results
| Method | nDCG@10 | MRR@10 | Recall@10 | Recall@100 |
|---|---:|---:|---:|---:|
| BM25 | 0.6318 | 0.5959 | 0.7598 | 0.8564 |
| Dense | 0.6451 | 0.6047 | 0.7833 | 0.9250 |
| Hybrid RRF, k=60 | **0.6684** | **0.6345** | **0.7938** | **0.9550** |

Hybrid over BM25: +0.0365 nDCG@10 (95% paired bootstrap CI for Hybrid−BM25: **[0.0138, 0.0594]**, Holm p=0.0042). Dense vs Hybrid nDCG difference was not statistically established (Holm p=0.1768).

### Slide 6 — Latency and trade-off
Median single-query latency, CPU: BM25 **15.90 ms**, Dense **12.56 ms**, Hybrid **31.48 ms** (p95: 30.24, 17.20, 50.21 ms). Hybrid's improved ranking vs BM25 costs about 1.98× the median latency. Uncached document embedding took 312.6 seconds once on this constrained runtime; the final rerun reused the local embedding cache. Plot: `results/plots/latency.png`.

### Slide 7 — Query-level evidence and failure modes
- BM25-only example: claim on CTCF anchor-site mutations; BM25 ranks relevant document 5373138 first, while Dense nDCG@10=0.
- Dense-only example: Bcl2/tumor maintenance claim; dense ranks the relevant BCL-2 leukemia paper first, while BM25 nDCG@10=0.
- Hybrid-only example: tamoxifen metabolism and breast-cancer outcomes; RRF ranks judged-relevant document 24341590 first.
- 33/300 queries had no relevant result in any system's top 10. Examples in `results/error_analysis/error_analysis.json`.

### Slide 8 — Findings, caveats, next steps
H1 is partly supported: RRF beats BM25 on key measures but is not significantly better than dense on nDCG@10. H3 is supported for Recall@100 on SciFact. H4 appears in measured CPU latency. Avoid generalizing beyond this claim/abstract task. Next: independently evaluate SciDocs or arXiv with a prespecified split and validation-only tuning. Existing WaterGPT UI and chatbot remain separate and unchanged.

**Reproducibility:** `research_study/README.md` · `EXPERIMENT_PROTOCOL.md` · complete results in `results/`.
