# Evaluating Lexical, Dense, and Hybrid Retrieval Methods for Scientific Literature Search

**Reproducible benchmark report · BEIR SciFact official test split · CPU execution**

## Abstract
We compare a lexical BM25 baseline, dense SentenceTransformers retrieval with exact FAISS cosine search, and Reciprocal Rank Fusion (RRF) of both systems on the official BEIR SciFact test benchmark. The benchmark comprises 5,183 documents and 300 test queries with 339 positive query-document judgments. All systems used identical title-plus-abstract text and candidate depth 1,000. Hybrid RRF achieved the highest measured macro nDCG@10 (0.6684) and Recall@100 (0.9550), compared with BM25 at 0.6318 and 0.8564. Paired bootstrap and Holm-corrected Wilcoxon analysis found a statistically supported nDCG@10 and Recall@100 improvement over BM25, but not over dense retrieval for nDCG@10. Hybrid median query latency was 32.0 ms, compared with 16.1 ms for BM25 and 12.8 ms for dense. These findings are limited to claim-to-abstract retrieval on SciFact and do not establish general scientific-search superiority.

## 1. Introduction and research question
Scientific search must retrieve evidence under vocabulary mismatch while retaining sensitivity to exact technical terminology, named entities, and phrases. This work asks: **Does combining traditional lexical retrieval with semantic vector retrieval improve scientific literature discovery compared with using either approach independently?** The preregistered-in-code hypotheses were that hybrid retrieval may improve ranking quality and coverage, dense retrieval may identify semantically relevant evidence missed lexically, and fusion may incur additional computational overhead. They are investigated rather than assumed.

WaterGPT already has an application-specific research-paper feature, but its corpus is not a standardized evaluation benchmark. This separate study tests a narrower question on official BEIR SciFact data and does not replace the chatbot's retrieval engine.

## 2. Related work
BM25 is a probabilistic lexical ranking model and a standard IR baseline (Robertson & Zaragoza, 2009). Sentence-BERT provides sentence embeddings suitable for semantic similarity (Reimers & Gurevych, 2019). FAISS provides vector similarity search, including exact inner-product indexes (Johnson et al., 2021). RRF is an established rank aggregation method proposed by Cormack et al. (2009); we apply, not invent, it. BEIR is a heterogeneous zero-shot retrieval benchmark (Thakur et al., 2021). SciFact was introduced for scientific claim verification and evidence retrieval (Wadden et al., 2020).

## 3. Dataset
The primary benchmark is official BEIR SciFact: 5,183 corpus documents, 1,109 total query records in the archive, and 300 queries selected by the official test qrels; the test qrels contain 339 positive judgments. Query and document IDs remain source strings. The corpus is scientific abstracts paired with claims in a claim-verification/evidence retrieval task. SciFact is not an arXiv-only collection or a broad sample of all scientific literature.

The original BEIR archive MD5 is `5f7d1de60b170fc8027bb7898e2efca1`; its SHA-256 and the SHA-256 of corpus, query, and test qrels files are stored in `results/metadata/dataset.json`. The official dataset host was unreachable from this runtime, so the download script retrieved the mirror of the original archive and verified it against BEIR's published MD5 before extraction. No raw data is committed. License signals differ across distributed representations: the SciFact source metadata identifies CC BY-NC 2.0, while the BEIR dataset card is marked CC BY-SA 4.0. Users should inspect the exact source and derivative terms before redistribution or commercial use; this study does not redistribute the dataset.

## 4. Methodology
Three independent systems share the dataset, test queries, query IDs, and title-plus-abstract content. BM25 uses `rank_bm25.BM25Okapi` with k1=1.5 and b=.75. Query and document text use the same lowercase alphanumeric tokenizer. Dense retrieval uses `sentence-transformers/all-MiniLM-L6-v2` (Reimers & Gurevych, 2019; Sentence Transformers model card); the loaded model emitted 384-dimensional vectors and exposed a maximum sequence length of 256 tokens in this run. Longer inputs are truncated by the model tokenizer. Vectors are normalized and cosine similarity is computed exactly through FAISS `IndexFlatIP`. The embedding cache is keyed by model, fields, corpus size, and a digest of source text.

Hybrid retrieval fuses the top-1,000 BM25 and dense rankings using RRF, `sum 1/(60 + rank)`, with one-based ranks. It does not combine uncalibrated raw scores. Ties break deterministically by document ID. Results are macro-averaged over all 300 test qrel queries. nDCG uses graded gain `2^rel-1`; MRR and recall use positive qrels. No test parameters were tuned. Ablations are descriptive held-out analyses only.

## 5. Experimental setup and metrics
Execution used Python 3.13.18, Linux x86_64, two logical CPUs, approximately 2.08 GB reported memory, and CPU-only PyTorch 2.9.1+cpu. Key package versions, selected device, model length, run configuration, and timing environment are recorded in `results/metadata/scifact-primary.json`. Every method was evaluated on the same 300 queries. The run stores component rankings, fused rankings, per-query metrics, and TREC-style runfiles.

Metrics are macro nDCG@10, MRR@10, Recall@10, and Recall@100. The implementation was tested against BEIR's `EvaluateRetrieval` nDCG and recall evaluator on a synthetic known fixture. Paired comparisons use 10,000 bootstrap resamples (seed 2026) and two-sided paired Wilcoxon tests with Holm correction across the three method contrasts within each metric. Latency measurements are single-query, with 10 warm-up queries and three repeated timing passes; 900 timed query observations are reported for each method. Model load, corpus embedding, index build, query embedding, BM25, FAISS, RRF, and end-to-end retrieval are separated in the JSON artifact.

## 6. Results

### 6.1 Retrieval effectiveness

| Method | nDCG@10 | MRR@10 | Recall@10 | Recall@100 |
|---|---:|---:|---:|---:|
| BM25 | 0.631820 | 0.595933 | 0.759833 | 0.856389 |
| Dense | 0.645082 | 0.604725 | 0.783333 | 0.925000 |
| Hybrid RRF (k=60) | **0.668365** | **0.634501** | **0.793778** | **0.955000** |

Hybrid led on all four aggregate metrics. Against BM25, the absolute gains were +0.0365 nDCG@10 (about 5.8% relative), +0.0386 MRR@10, +0.0339 Recall@10, and +0.0986 Recall@100. Dense retrieval was above BM25 on the four aggregate point estimates, with the clearest gain at Recall@100 (+0.0686).

### 6.2 Paired uncertainty and significance
Differences below are `method_a − method_b`; negative values therefore favor method_b.

| Outcome / contrast | Mean difference | 95% paired bootstrap CI | Holm-adjusted p |
|---|---:|---:|---:|
| nDCG@10: BM25 − Dense | −0.01326 | [−0.05231, 0.02681] | 0.7497 |
| nDCG@10: BM25 − Hybrid | −0.03654 | [−0.05940, −0.01375] | 0.0042 |
| nDCG@10: Dense − Hybrid | −0.02328 | [−0.05219, 0.00578] | 0.1768 |
| MRR@10: BM25 − Hybrid | −0.03857 | [−0.06553, −0.01099] | 0.0141 |
| Recall@100: BM25 − Dense | −0.06861 | [−0.11222, −0.02706] | 0.0077 |
| Recall@100: BM25 − Hybrid | −0.09861 | [−0.13333, −0.06700] | 2.29×10⁻⁷ |
| Recall@100: Dense − Hybrid | −0.03000 | [−0.05667, −0.00667] | 0.0201 |

The nDCG@10 improvement of hybrid over BM25 is supported by the paired interval and corrected test. The hybrid-versus-dense nDCG interval includes zero and corrected p=0.1768, so the benchmark does not establish that hybrid is more effective than dense retrieval at this cutoff. Dense and hybrid both improved Recall@100 over BM25 in this sample; hybrid also exceeded dense. Recall@10's hybrid-vs-BM25 raw p=0.0345 did not survive Holm correction (adjusted p=0.1035). Statistical evidence is outcome- and comparison-specific and does not prove broad generalization.

### 6.3 Latency and computational cost

| Method | Mean (ms) | Median (ms) | p95 (ms) |
|---|---:|---:|---:|
| BM25 | 17.26 | 15.90 | 30.24 |
| Dense | 12.71 | 12.56 | 17.20 |
| Hybrid RRF | 32.99 | 31.48 | 50.21 |

In this CPU-limited runtime, hybrid median query latency was approximately 1.98× BM25 and 2.51× dense. Component means in the repeated evaluation were 13.24 ms query embedding, 0.65 ms FAISS search, 1.84 ms RRF fusion, and 18.93 ms BM25 processing. One-time model load was 1.33 s; an uncached embedding observation took 312.56 s for 5,183 documents. The final run reused the local embedding cache (0 s corpus encoding in that rerun). BM25 index build in the final run was 0.53 s and FAISS index construction 0.0016 s. Both warm-cache and uncached timing information are reflected in the latency artifacts. These values are environment-specific; two logical CPUs and limited RAM constrain general latency interpretation.

## 7. Error analysis
There were 33/300 queries where all three methods had zero nDCG@10; these are top-10 failures, not claims about all possible retrieval depths. A BM25-only winner was query 1024, “Recurrent mutations occur frequently within CTCF anchor sites adjacent to oncogenes.” BM25 placed relevant document 5373138, “3D Chromosome Regulatory Landscape of Human Pluripotent Cells,” at rank 1 (qrel=1); dense nDCG@10 was 0. A dense-only winner was query 1088, “Silencing of Bcl2 is important for the maintenance and progression of tumors.” Dense retrieved relevant document 37549932, “Antiapoptotic BCL-2 is required for maintenance of a model leukemia,” first (qrel=1), while BM25 nDCG@10 was 0. For query 1259 on tamoxifen metabolism and breast-cancer treatment outcome, hybrid placed relevant document 24341590 first; the two component systems had nDCG@10 0.50 and 0.63, while hybrid was 1.0.

One all-system top-10 miss was query 13, “5% of perinatal mortality is due to low birth weight.” The returned document titles concern neonatal/perinatal mortality, but none of those top-10 document IDs was positively judged. This illustrates that topical plausibility is not equivalent to qrel relevance. Examples and scores are saved in `results/error_analysis/error_analysis.json`; similarity or BM25 scores are not evidence of model understanding.

## 8. Ablations

| Ablation | Setting | nDCG@10 | MRR@10 | Recall@10 | Recall@100 |
|---|---|---:|---:|---:|---:|
| RRF k | 20 | 0.679045 | 0.641282 | 0.816111 | 0.955000 |
| RRF k | 60 (primary) | 0.668365 | 0.634501 | 0.793778 | 0.955000 |
| RRF k | 100 | 0.670001 | 0.634840 | 0.800444 | 0.948333 |
| Text fields | title-only Hybrid, k=60 | 0.506888 | 0.483058 | 0.619889 | 0.854333 |

The title-only results were lower than title-plus-abstract, emphasizing the contribution of abstract text in this task. k=20 had the highest reported RRF nDCG@10 among the tested held-out settings, but this is a descriptive test-set observation and must not be used to claim tuned/generalizable superiority. Candidate depth 100, 500, and 1,000 produced nDCG@10 0.667548, 0.668325, and 0.668365 respectively; depth 100's Recall@100 is 0.957 because truncating component lists changes the fused ranking. Full ablation rows are in `results/metrics/ablation_results.csv`.

## 9. Discussion and hypotheses
H1 is **partially supported**: hybrid improves over BM25 on nDCG@10 and MRR@10 under corrected paired tests and on Recall@100, but it was not significantly better than dense on nDCG@10. H2 is **supported by query-level examples but not established as an aggregate advantage over BM25**: dense had 45 unique nDCG@10 query wins, but aggregate nDCG difference vs BM25 was not significant. H3 is **supported for Recall@100** in this benchmark; hybrid achieved 0.955 and was significantly above both individual systems in paired tests. H4 is **supported operationally on this CPU run**: hybrid had higher median end-to-end query latency than either component. These findings concern only this configuration and benchmark.

## 10. Limitations and threats to validity
SciFact is small, English-language, claim-to-abstract evidence retrieval; it does not demonstrate performance for full-text search, multilingual literature, all disciplines, or WaterGPT production traffic. Qrels can be incomplete: unjudged retrieved documents are not treated as relevant. The test qrels include 300 queries, each with positive judgments; the evaluator supports zero-positive cases, but none were present in this split. MiniLM truncates longer texts at the loaded model maximum. The BM25 configuration is conventional and fixed rather than tuned on validation. Held-out ablations are descriptive, not model selection. Latency depends on hardware, thread scheduling and implementation details. Bootstrap/Wilcoxon inference is conditional on the benchmark's finite queries and does not prove generalizable causal superiority.

## 11. Conclusion
On SciFact test, BM25 and dense retrieval each contribute useful rankings, and fixed-k RRF improves the measured aggregate metrics, with statistically supported gains over BM25 in nDCG@10 and Recall@100. Hybrid did not demonstrate a significant nDCG@10 advantage over dense retrieval, and incurs additional CPU query latency. The study therefore provides nuanced support for complementary retrieval signals rather than a universal claim that hybrid search is best. A separately reported SciDocs or arXiv-domain evaluation is needed before discussing cross-domain generalization.

## References
See `references.bib` for full bibliographic entries. Key works: Wadden et al. (2020), Thakur et al. (2021), Cormack et al. (2009), Reimers & Gurevych (2019), Robertson & Zaragoza (2009), and Johnson et al. (2021).
