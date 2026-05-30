import os
import sys
from pathlib import Path

import pandas as pd


# Make backend root importable when running from scripts/
BACKEND_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(BACKEND_ROOT))

from utils.rag_engine import RAGEngine
from utils.updater import KnowledgeUpdater


DATA_DIR = BACKEND_ROOT / "data"
MEDQUAD_PATH = DATA_DIR / "medquad.csv"
ARXIV_PATH = DATA_DIR / "arxiv_subset.csv"
KNOWLEDGE_PATH = DATA_DIR / "knowledge.txt"


def safe_get(row, possible_columns):
    """
    Returns first existing non-empty value from possible column names.
    This makes the script work even if your CSV column names are different.
    """
    for col in possible_columns:
        if col in row and pd.notna(row[col]):
            value = str(row[col]).strip()
            if value:
                return value
    return ""


def load_medquad():
    """
    Loads MedQuAD CSV and converts each row into a RAG document.
    Expected columns may be:
    - question / answer
    - Question / Answer
    - q / a
    - question_text / answer_text
    """

    if not MEDQUAD_PATH.exists():
        print(f"[SKIP] MedQuAD file not found: {MEDQUAD_PATH}")
        return [], []

    print(f"[LOAD] Reading MedQuAD: {MEDQUAD_PATH}")

    df = pd.read_csv(MEDQUAD_PATH)
    texts = []
    metadata = []

    for idx, row in df.iterrows():
        question = safe_get(
            row,
            [
                "question",
                "Question",
                "QUESTION",
                "q",
                "Q",
                "question_text",
                "Question Text",
            ],
        )

        answer = safe_get(
            row,
            [
                "answer",
                "Answer",
                "ANSWER",
                "a",
                "A",
                "answer_text",
                "Answer Text",
            ],
        )

        source = safe_get(
            row,
            [
                "source",
                "Source",
                "url",
                "URL",
                "file",
                "File",
            ],
        )

        # If no clear question/answer columns exist, combine all row text
        if not question and not answer:
            combined = " ".join(
                [
                    str(value).strip()
                    for value in row.values
                    if pd.notna(value) and str(value).strip()
                ]
            )
        else:
            combined = f"Medical Question: {question}\nMedical Answer: {answer}"

        if combined.strip():
            texts.append(combined)
            metadata.append(
                {
                    "source": "medquad",
                    "type": "medical_qa",
                    "row": int(idx),
                    "original_source": source,
                }
            )

    print(f"[OK] Loaded {len(texts)} MedQuAD documents")
    return texts, metadata


def load_arxiv():
    """
    Loads arXiv subset CSV and converts each paper into a RAG document.
    Expected columns may be:
    - title
    - abstract
    - summary
    - categories
    - authors
    """

    if not ARXIV_PATH.exists():
        print(f"[SKIP] arXiv file not found: {ARXIV_PATH}")
        return [], []

    print(f"[LOAD] Reading arXiv: {ARXIV_PATH}")

    df = pd.read_csv(ARXIV_PATH)
    texts = []
    metadata = []

    for idx, row in df.iterrows():
        title = safe_get(row, ["title", "Title", "TITLE"])
        abstract = safe_get(
            row,
            [
                "abstract",
                "Abstract",
                "summary",
                "Summary",
                "description",
                "Description",
            ],
        )

        authors = safe_get(row, ["authors", "Authors"])
        categories = safe_get(row, ["categories", "category", "Category"])
        paper_id = safe_get(row, ["id", "paper_id", "arxiv_id", "ID"])

        # If no expected columns exist, combine all row text
        if not title and not abstract:
            combined = " ".join(
                [
                    str(value).strip()
                    for value in row.values
                    if pd.notna(value) and str(value).strip()
                ]
            )
        else:
            combined = (
                f"Research Paper Title: {title}\n"
                f"Authors: {authors}\n"
                f"Categories: {categories}\n"
                f"Abstract: {abstract}"
            )

        if combined.strip():
            texts.append(combined)
            metadata.append(
                {
                    "source": "arxiv",
                    "type": "research_paper",
                    "row": int(idx),
                    "paper_id": paper_id,
                    "title": title,
                    "categories": categories,
                }
            )

    print(f"[OK] Loaded {len(texts)} arXiv documents")
    return texts, metadata


def load_knowledge_text(updater):
    """
    Loads knowledge.txt and chunks it.
    """

    if not KNOWLEDGE_PATH.exists():
        print(f"[SKIP] knowledge.txt file not found: {KNOWLEDGE_PATH}")
        return [], []

    print(f"[LOAD] Reading knowledge.txt: {KNOWLEDGE_PATH}")

    content = KNOWLEDGE_PATH.read_text(encoding="utf-8", errors="ignore")
    chunks = updater.chunk_text(content, chunk_size=500, overlap=50)

    metadata = [
        {
            "source": "knowledge_txt",
            "type": "general_knowledge",
            "chunk": i,
        }
        for i in range(len(chunks))
    ]

    print(f"[OK] Loaded {len(chunks)} chunks from knowledge.txt")
    return chunks, metadata


def add_in_batches(rag, texts, metadata, batch_size=128):
    """
    Adds documents to FAISS in batches.
    """

    total = len(texts)

    if total == 0:
        return 0

    added = 0

    for start in range(0, total, batch_size):
        end = start + batch_size

        batch_texts = texts[start:end]
        batch_metadata = metadata[start:end]

        count = rag.add_documents(batch_texts, batch_metadata, save=False)
        added += count

        print(f"[INDEX] Added {added}/{total}")

    return added


def main():
    print("=" * 70)
    print("waterGPT FAISS Index Builder")
    print("=" * 70)

    rag = RAGEngine()
    updater = KnowledgeUpdater(rag=rag)

    print("\n[RESET] Clearing existing FAISS index...")
    rag.clear_index()

    grand_total = 0

    print("\n[1/3] Loading MedQuAD...")
    medquad_texts, medquad_metadata = load_medquad()
    grand_total += add_in_batches(
        rag,
        medquad_texts,
        medquad_metadata,
        batch_size=128,
    )

    print("\n[2/3] Loading arXiv...")
    arxiv_texts, arxiv_metadata = load_arxiv()
    grand_total += add_in_batches(
        rag,
        arxiv_texts,
        arxiv_metadata,
        batch_size=128,
    )

    print("\n[3/3] Loading knowledge.txt...")
    knowledge_texts, knowledge_metadata = load_knowledge_text(updater)
    grand_total += add_in_batches(
        rag,
        knowledge_texts,
        knowledge_metadata,
        batch_size=128,
    )

    print("\n[SAVE] Saving final FAISS index...")
    rag.save_index()

    print("\n" + "=" * 70)
    print(f"[DONE] Total indexed documents/chunks: {grand_total}")
    print(f"[SAVE] FAISS index saved to: {rag.index_path}")
    print("=" * 70)


if __name__ == "__main__":
    main()