import os
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"
STORAGE_DIR = BASE_DIR / "storage"
UPLOAD_DIR = BASE_DIR / "uploads"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
MODEL_NAME = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")

VISION_MODEL_PRIMARY = os.getenv(
    "VISION_MODEL_PRIMARY",
    "meta-llama/llama-4-scout-17b-16e-instruct",
)

VISION_MODEL_FALLBACK = os.getenv(
    "VISION_MODEL_FALLBACK",
    "meta-llama/llama-4-maverick-17b-128e-instruct",
)

# --- Google Gemini configuration (Multi-Modal Chatbot task) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GEMINI_VISION_MODEL = os.getenv(
    "GEMINI_VISION_MODEL",
    "gemini-2.5-flash",
)

GEMINI_IMAGE_MODEL = os.getenv(
    "GEMINI_IMAGE_MODEL",
    "gemini-2.5-flash-image",
)

EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

FAISS_INDEX_PATH = os.getenv(
    "FAISS_INDEX_PATH",
    str(STORAGE_DIR / "faiss_index"),
)

FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")

GENERATED_IMAGES_DIR = STORAGE_DIR / "generated_images"

DATA_DIR.mkdir(parents=True, exist_ok=True)
STORAGE_DIR.mkdir(parents=True, exist_ok=True)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
GENERATED_IMAGES_DIR.mkdir(parents=True, exist_ok=True)