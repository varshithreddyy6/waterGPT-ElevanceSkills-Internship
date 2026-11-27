# Figure captions

1. **effectiveness.png — Retrieval effectiveness.** Macro nDCG@10, MRR@10, Recall@10 and Recall@100 for BM25, dense retrieval, and fixed-k hybrid RRF on 300 official SciFact test queries.
2. **ndcg_mrr.png — Top-rank quality.** Macro nDCG@10 and MRR@10 comparison.
3. **recall.png — Retrieval coverage.** Macro Recall@10 and Recall@100 comparison.
4. **latency.png — Steady-state latency.** Mean, median and p95 single-query latency from 900 measured query observations per method after warm-up; values are CPU-specific.
5. **per_query_distribution.png — Per-query outcomes.** Distribution of query-level nDCG@10; macro aggregate alone can hide per-query variation.
6. **confidence_intervals.png — Paired comparisons.** Mean method-A minus method-B difference and percentile 95% paired bootstrap intervals for each metric; zero-reference line marks no mean difference.
7. **ablation.png — Held-out descriptive ablations.** RRF k and component candidate-depth sensitivity, plus title-only versus title+abstract results. These are not used to tune primary settings.
