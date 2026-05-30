import os

# Force Hugging Face / Transformers to use local cache.
# This prevents backend startup from failing when internet is unstable.
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from config import EMBEDDING_MODEL, FAISS_INDEX_PATH


class RAGEngine:
    def __init__(self):
        self.index_path = FAISS_INDEX_PATH
        self.dimension = 384
        self.index = None
        self.documents = []

        os.makedirs(self.index_path, exist_ok=True)

        print(f"Loading embedding model: {EMBEDDING_MODEL}")

        try:
            self.embedding_model = SentenceTransformer(
                EMBEDDING_MODEL,
                local_files_only=True,
            )
            print("Embedding model loaded from local cache")
        except TypeError:
            # For older sentence-transformers versions that may not accept local_files_only
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)
            print("Embedding model loaded")
        except Exception as e:
            print(f"Offline model loading failed: {e}")
            print("Trying normal model loading...")
            self.embedding_model = SentenceTransformer(EMBEDDING_MODEL)

        self.load_index()

    def load_index(self):
        index_file = os.path.join(self.index_path, "index.faiss")
        docs_file = os.path.join(self.index_path, "documents.pkl")

        if os.path.exists(index_file) and os.path.exists(docs_file):
            self.index = faiss.read_index(index_file)

            with open(docs_file, "rb") as f:
                self.documents = pickle.load(f)

            print(f"Loaded FAISS index with {len(self.documents)} documents")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            print("Created new FAISS index")

    def save_index(self):
        faiss.write_index(
            self.index,
            os.path.join(self.index_path, "index.faiss"),
        )

        with open(os.path.join(self.index_path, "documents.pkl"), "wb") as f:
            pickle.dump(self.documents, f)

        print(f"Saved FAISS index with {len(self.documents)} documents")

    def add_documents(self, texts, metadata=None, save=True):
        texts = [text for text in texts if text and text.strip()]

        if not texts:
            return 0

        embeddings = self.embedding_model.encode(
            texts,
            show_progress_bar=False,
        )

        embeddings = np.array(embeddings).astype("float32")
        self.index.add(embeddings)

        for i, text in enumerate(texts):
            doc_metadata = metadata[i] if metadata and i < len(metadata) else {}

            self.documents.append(
                {
                    "text": text,
                    "metadata": doc_metadata,
                }
            )

        if save:
            self.save_index()

        return len(texts)

    def search(self, query, top_k=3):
        if not query or self.index.ntotal == 0:
            return []

        query_embedding = self.embedding_model.encode([query]).astype("float32")

        distances, indices = self.index.search(
            query_embedding,
            min(top_k, self.index.ntotal),
        )

        results = []

        for idx, dist in zip(indices[0], distances[0]):
            if 0 <= idx < len(self.documents):
                results.append(
                    {
                        "text": self.documents[idx].get("text", ""),
                        "metadata": self.documents[idx].get("metadata", {}),
                        "score": float(dist),
                    }
                )

        return results

    def clear_index(self):
        self.index = faiss.IndexFlatL2(self.dimension)
        self.documents = []
        self.save_index()