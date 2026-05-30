import time
import urllib.parse
from pathlib import Path

import feedparser
import pandas as pd


BACKEND_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = BACKEND_ROOT / "data"
OUTPUT_FILE = DATA_DIR / "arxiv_subset.csv"


ARXIV_API_URL = "http://export.arxiv.org/api/query"

# arXiv categories useful for this project
CATEGORIES = [
    "cs.AI",   # Artificial Intelligence
    "cs.CL",   # Computation and Language
    "cs.LG",   # Machine Learning
    "cs.IR",   # Information Retrieval
    "cs.CV",   # Computer Vision
]

PAPERS_PER_CATEGORY = 100

# arXiv recommends not sending requests too fast
REQUEST_DELAY_SECONDS = 3


def clean_text(text):
    if not text:
        return ""

    return " ".join(text.replace("\n", " ").split())


def fetch_arxiv_category(category, max_results=100):
    print(f"[FETCH] Category: {category} | Papers: {max_results}")

    query = f"cat:{category}"

    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }

    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"

    feed = feedparser.parse(url)

    rows = []

    for entry in feed.entries:
        paper_id = entry.get("id", "").split("/abs/")[-1]

        title = clean_text(entry.get("title", ""))
        abstract = clean_text(entry.get("summary", ""))

        authors = ", ".join(
            [author.get("name", "") for author in entry.get("authors", [])]
        )

        published = entry.get("published", "")
        updated = entry.get("updated", "")

        link = entry.get("link", "")

        categories = []

        for tag in entry.get("tags", []):
            term = tag.get("term")
            if term:
                categories.append(term)

        rows.append(
            {
                "id": paper_id,
                "title": title,
                "authors": authors,
                "categories": ", ".join(categories),
                "primary_category": category,
                "abstract": abstract,
                "published": published,
                "updated": updated,
                "link": link,
            }
        )

    print(f"[OK] Retrieved {len(rows)} papers from {category}")
    return rows


def main():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    all_rows = []

    print("=" * 70)
    print("waterGPT arXiv Subset Downloader")
    print("=" * 70)

    for category in CATEGORIES:
        rows = fetch_arxiv_category(
            category=category,
            max_results=PAPERS_PER_CATEGORY,
        )

        all_rows.extend(rows)

        print(f"[WAIT] Sleeping {REQUEST_DELAY_SECONDS}s to respect arXiv API")
        time.sleep(REQUEST_DELAY_SECONDS)

    df = pd.DataFrame(all_rows)

    before = len(df)

    df = df.drop_duplicates(subset=["id"])

    after = len(df)

    df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8",
    )

    print("\n" + "=" * 70)
    print(f"[DONE] Saved arXiv subset to: {OUTPUT_FILE}")
    print(f"[INFO] Papers before duplicate removal: {before}")
    print(f"[INFO] Papers after duplicate removal: {after}")
    print("=" * 70)


if __name__ == "__main__":
    main()