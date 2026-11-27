# Methodology

## Retrieval systems
The lexical baseline is `rank_bm25.BM25Okapi`, configured with k1=1.5 and b=.75. Both query and indexed text are lowercased and tokenized with the same stable alphanumeric regex. Document text is title plus abstract (`text` in BEIR), preserving the title and body as a space-joined field.

Dense retrieval uses the public `sentence-transformers/all-MiniLM-L6-v2` encoder. Its model-card dimension is 384; inputs longer than the model's configured maximum sequence length are truncated by SentenceTransformers. Document and query vectors are normalized and searched exactly using FAISS `IndexFlatIP`, making inner product equal cosine similarity. The default device is SentenceTransformers' automatic device selection (CPU where no accelerator is available); the selected device is recorded.

Hybrid retrieval applies Reciprocal Rank Fusion to independently produced BM25 and dense rank lists: sum `1/(60+rank)` at 1-based ranks. Component candidate depth is 1,000, final run depth is capped by available candidates. Deterministic document-ID tie breaks are used. Scores are not calibrated or blended.

## Data and evaluation
Official BEIR SciFact corpus, queries, test qrels. Query/doc IDs remain strings from source. Integrity validator checks required files, count ranges, unique IDs, qrel query existence and positive qrel document existence. Per-query nDCG uses graded gain `2^rel-1`; MRR uses the first positive document; recall is binary over positive qrel docs. Macro means retain any qrel query with no positive judgments as zero.

## Statistics and latency
Each method is compared on paired query outcomes. Bootstrap resamples paired query indices 10,000 times with seed 2026; percentile 95% interval of the mean difference. Two-sided Wilcoxon signed-rank results are adjusted with Holm's step-down procedure within reported metric family. These tests do not imply causal superiority beyond this benchmark. Index build, model load, corpus encoding, query encoding, FAISS, BM25, RRF, and end-to-end latency are logged separately where available. Timing uses single queries, explicit warm-ups and repeated runs.

## Implementation boundary
BEIR and SciFact are existing benchmark/framework contributions; BM25, SentenceTransformers, FAISS and RRF are established tools/algorithms. The project contribution is their independent, controlled integration and reproducible evaluation with preserved IDs, raw runs, per-query analysis, and transparent reporting—not a new retrieval algorithm.
