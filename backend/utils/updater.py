import os
import time
from datetime import datetime

import requests
import schedule
from bs4 import BeautifulSoup

from utils.rag_engine import RAGEngine


class KnowledgeUpdater:
    def __init__(self, rag=None):
        self.rag = rag or RAGEngine()
        self.sources = []

    def add_source(self, url, source_type="web"):
        self.sources.append(
            {
                "url": url,
                "type": source_type,
            }
        )

    def fetch_web_content(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0",
            }

            response = requests.get(
                url,
                headers=headers,
                timeout=15,
            )

            response.raise_for_status()

            soup = BeautifulSoup(response.content, "html.parser")

            for tag in soup(["script", "style", "nav", "footer"]):
                tag.decompose()

            text = soup.get_text()

            lines = [
                line.strip()
                for line in text.splitlines()
                if line.strip()
            ]

            return " ".join(lines)

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return ""

    def chunk_text(self, text, chunk_size=500, overlap=50):
        words = (text or "").split()

        if not words:
            return []

        chunks = []
        step = max(chunk_size - overlap, 1)

        for i in range(0, len(words), step):
            chunk = " ".join(words[i:i + chunk_size])

            if chunk.strip():
                chunks.append(chunk)

        return chunks

    def update_from_file(self, file_path):
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return 0

        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        chunks = self.chunk_text(content)

        metadata = [
            {
                "source": file_path,
                "type": "file",
                "updated": str(datetime.now()),
            }
            for _ in chunks
        ]

        return self.rag.add_documents(chunks, metadata)

    def update_from_url(self, url):
        content = self.fetch_web_content(url)

        if not content:
            return 0

        chunks = self.chunk_text(content)

        metadata = [
            {
                "source": url,
                "type": "url",
                "updated": str(datetime.now()),
            }
            for _ in chunks
        ]

        return self.rag.add_documents(chunks, metadata)

    def update_all_sources(self):
        print(f"Updating knowledge base at {datetime.now()}")

        total = 0

        for source in self.sources:
            if source["type"] == "web":
                total += self.update_from_url(source["url"])

            elif source["type"] == "file":
                total += self.update_from_file(source["url"])

        print(f"Added {total} new chunks")

        return total

    def schedule_updates(self, interval_hours=24):
        schedule.every(interval_hours).hours.do(self.update_all_sources)

        while True:
            schedule.run_pending()
            time.sleep(60)