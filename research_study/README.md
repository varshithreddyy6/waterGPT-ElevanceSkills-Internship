# Reproducible scientific retrieval study

**Evaluating Lexical, Dense, and Hybrid Retrieval Methods for Scientific Literature Search**

This standalone CLI study tests whether Reciprocal Rank Fusion of BM25 and semantic dense retrieval improves retrieval of scientific evidence over either method alone. It is independent of WaterGPT's chatbot runtime, existing arXiv retrieval engine, and any Gemini/Groq credentials. Existing frontend/UI files are not part of this workspace.

## Research question and objectives

Does combining lexical and semantic ranking improve scientific literature discovery? Objectives: establish BM25 and dense baselines; implement exact dense cosine search; fuse ranks with RRF; measure effectiveness, latency, paired uncertainty, and query-level disagreements; report limitations transparently.

## Benchmark
Official [BEIR SciFact](https://github.com/beir-cellar/beir) download, test split, qrels and full corpus. SciFact is a claim-to-evidence retrieval benchmark with 5,183 abstracts and 300 official test claims (the archive also has train/dev query records). It is not a generic literature-search sample and cannot support claims of broad cross-discipline generalization. Data is fetched from the BEIR dataset host; if that host is unavailable, the downloader accepts a third-party mirror only after validating the original BEIR-published archive MD5. Current license metadata differs across representations: the upstream SciFact metadata identifies CC BY-NC 2.0, while the BEIR Hugging Face dataset card lists CC BY-SA 4.0. Verify applicable terms from the exact original source before reuse, attribution, or redistribution; this repository does not commit the raw dataset. Checksums and test-split counts are recorded in `results/metadata/dataset.json`.

## Scientific contributions

This project contributes a reproducible experimental implementation and analysis—not a new retrieval algorithm. BM25, SentenceTransformers, FAISS, BEIR/SciFact, and RRF are existing methods, libraries, and benchmarks. The implementation contribution is controlled, ID-preserving comparison; validated metrics and paired statistics; saved ranked runs; latency decomposition; and query-level error/ablation artifacts.

## Architecture

- `src/data_loader.py`: download-layout discovery, JSONL/TSV parsing, record and qrel integrity.
- `src/preprocessing.py`: shared lowercase tokenization and title/text composition.
- `src/lexical_retrieval.py`: BM25Okapi.
- `src/dense_retrieval.py`: SentenceTransformers `all-MiniLM-L6-v2`, normalized vectors, exact FAISS inner product, local embedding cache.
- `src/hybrid_retrieval.py`: independent deterministic RRF (k=60).
- `src/evaluation.py`, `statistics.py`, `latency.py`, `error_analysis.py`: macro metrics, paired statistics, timing and real document examples.
- `scripts/`: download, validate, run, ablate, and plot-generation commands.

## Setup and commands

Run from this directory with Python 3.10+ recommended (the dependency set has been pinned and isolated from WaterGPT):

```bash
python -m venv .venv
. .venv/bin/activate                 # Windows: .venv\\Scripts\\activate
python -m pip install --upgrade pip
# CPU-only Linux install (avoids pulling CUDA toolkit dependencies):
python -m pip install 'torch==2.9.1' --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r requirements.txt
python scripts/download_dataset.py
python scripts/validate_dataset.py
pytest -q
python scripts/run_experiments.py
python scripts/run_ablation.py
python scripts/generate_report.py
python scripts/create_presentation.py
python scripts/audit_results.py
```

Optional GPU: pass `--device cuda` when PyTorch/CUDA are compatible. The default is CPU. First dense run downloads the public model weights and creates a local cache under `data/cache/`.

## Configuration / metrics

`configs/default.yaml` fixes BM25 k1=1.5,b=.75, common tokenizer, title+abstract, top-1000 component depth, MiniLM-L6-v2, RRF k=60, seed 2026, and 10,000 bootstrap resamples. Main evaluation uses official test qrels without parameter tuning. Macro nDCG@10, MRR@10, Recall@10 and Recall@100; qrel queries without positive judgments receive zero and remain in the denominator. RRF is rank-based, not score blending. See `EXPERIMENT_PROTOCOL.md`.

## Outputs

Measured CSV tables, per-query metrics, compressed TREC runfiles (`.trec.gz`), component rankings, run configuration, timing/environment metadata, paired bootstrap/Wilcoxon results, error examples and plots are stored in `results/`.

| Method | nDCG@10 | MRR@10 | Recall@10 | Recall@100 |
|---|---:|---:|---:|---:|
| BM25 | 0.631820 | 0.595933 | 0.759833 | 0.856389 |
| Dense | 0.645082 | 0.604725 | 0.783333 | 0.925000 |
| Hybrid RRF (k=60) | **0.668365** | **0.634501** | **0.793778** | **0.955000** |

These are the measured macro scores for 300 official test queries. The paired nDCG@10 difference favors hybrid over BM25 by 0.03654 (95% paired bootstrap CI for Hybrid−BM25 [0.01375, 0.05940], Holm-adjusted p=0.0042); hybrid versus dense was not significant on nDCG@10 (adjusted p=0.1768). Hybrid median CPU latency was 31.48 ms; see the full latency report and caveats. Plots: `results/plots/effectiveness.png`, `results/plots/latency.png`, `results/plots/confidence_intervals.png`, and `results/plots/ablation.png`. The detailed report, 8-slide Markdown outline, and editable 8-slide PowerPoint (`reports/presentation.pptx`) live under `reports/`. Seven charts are in `results/plots/`: effectiveness, nDCG/MRR, recall, latency, per-query distribution, paired confidence intervals, and ablations. Never interpret placeholder or missing output as experimental evidence.

## Limitations

SciFact is small and focused on claims and abstracts; relevance is sparse and benchmark-specific. MiniLM truncates inputs to its configured model sequence limit. CPU/GPU and BLAS/FAISS details affect latency. Paired test-set analyses are descriptive inference, not proof of universal superiority. Ablations are held-out descriptive comparisons and not tuning.

## Attribution

BEIR: Thakur et al. (2021); SciFact: Wadden et al. (2020); RRF: Cormack et al. (2009); SentenceTransformers: Reimers & Gurevych (2019). Full citations: `reports/references.bib`.
