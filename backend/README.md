# waterGPT Backend

The waterGPT Backend is the core processing layer of the waterGPT project. It is built using **FastAPI** and provides APIs for chat, medical question answering, research assistance, image understanding, voice transcription, sentiment analysis, multilingual communication, and dynamic knowledge base management.

Developed as part of the **Elevance Skills Internship**, the backend combines Retrieval-Augmented Generation (RAG), vector search, Large Language Models, and multiple AI services into a unified architecture.

---

# Overview

The backend acts as the central intelligence layer of the system.

Its responsibilities include:

* Processing user requests
* Managing AI model communication
* Performing semantic retrieval
* Handling image analysis
* Processing voice input
* Managing multilingual translation
* Updating knowledge bases
* Serving frontend applications

Both the Streamlit interface and the Next.js frontend communicate with this backend through REST APIs.

---

# Core Features

## General Chat

Provides conversational AI capabilities using Groq-hosted Llama models.

Features:

* Multi-turn conversations
* Context-aware responses
* Natural language understanding
* Follow-up question handling

---

## Medical Question Answering

Uses the MedQuAD dataset and Retrieval-Augmented Generation.

Features:

* Medical knowledge retrieval
* Symptom explanations
* Disease information
* Treatment-related information
* Medical entity recognition

The backend retrieves relevant medical content before generating responses.

---

## Research Assistant

Uses arXiv research papers as a scientific knowledge source.

Features:

* Research paper retrieval
* Scientific concept explanation
* Technical Q&A
* Research summarization

Supported areas include:

* Artificial Intelligence
* Machine Learning
* Natural Language Processing
* Information Retrieval
* Computer Vision

---

## Vision AI

Supports image understanding using vision-capable AI models.

Features:

* Image upload processing
* Visual question answering
* Object identification
* Scene understanding
* Contextual image explanations

---

## Voice Transcription

Supports voice-enabled interaction.

Features:

* Audio upload
* Speech-to-text conversion
* Chat integration
* Voice query processing

Powered by Groq Whisper models.

---

## Dynamic Knowledge Base

Allows users to continuously expand chatbot knowledge.

Supported sources:

* URLs
* Plain text
* TXT files
* CSV files
* Markdown files
* PDF documents

Uploaded content is automatically:

1. Extracted
2. Cleaned
3. Chunked
4. Embedded
5. Indexed in FAISS

---

## Sentiment Analysis

Detects user sentiment.

Supported classes:

* Positive
* Neutral
* Negative

Used for:

* Analytics
* Conversation monitoring
* Adaptive responses

---

## Multilingual Support

Supports multilingual communication through translation and language detection.

Workflow:

```text
User Input
     ↓
Language Detection
     ↓
Translation to English
     ↓
Retrieval + Generation
     ↓
Translation to Target Language
     ↓
Final Response
```

---

# Technology Stack

## Backend Framework

* FastAPI

## Programming Language

* Python

## AI Provider

* Groq API

## Vector Database

* FAISS

## Embeddings

* SentenceTransformers

## Sentiment Analysis

* VADER

## Translation

* Deep Translator
* Langdetect

## Vision Processing

* Pillow

## Web Parsing

* BeautifulSoup

## Research Data Collection

* Feedparser

## PDF Processing

* pypdf

---

# AI Models

## Text Generation

```text
llama-3.3-70b-versatile
```

Used for:

* General chat
* Medical responses
* Research explanations

---

## Vision Understanding

Primary Model:

```text
meta-llama/llama-4-scout-17b-16e-instruct
```

Fallback Model:

```text
meta-llama/llama-4-maverick-17b-128e-instruct
```

Used for:

* Image analysis
* Visual reasoning
* Image question answering

---

## Voice Transcription

```text
whisper-large-v3
```

Used for:

* Audio transcription
* Speech-to-text conversion

---

## Embedding Model

```text
all-MiniLM-L6-v2
```

Used for:

* Semantic search
* Similarity matching
* Vector retrieval

---

# Backend Architecture

```text
User
 |
 v
Frontend
 |
 v
FastAPI Backend
 |
 +----------------------+
 |                      |
 v                      v
Chat Service       Vision Service
 |                      |
 v                      v
RAG Engine         Vision Models
 |
 v
FAISS Database
 |
 +---------------------------+
 |             |             |
 v             v             v
MedQuAD     arXiv      User Knowledge
```

---

# Folder Structure

```text
backend
│
├── api
│   ├── __init__.py
│   ├── chat.py
│   ├── vision.py
│   ├── knowledge.py
│   ├── analytics.py
│   └── settings.py
│
├── core
│   ├── __init__.py
│   ├── groq_client.py
│   ├── prompts.py
│   └── state.py
│
├── schemas
│   ├── __init__.py
│   ├── chat.py
│   ├── knowledge.py
│   ├── vision.py
│   └── analytics.py
│
├── services
│   ├── __init__.py
│   ├── chat_service.py
│   ├── vision_service.py
│   ├── knowledge_service.py
│   ├── analytics_service.py
│   ├── settings_service.py
│   └── medical_ner_service.py
│
├── utils
│   ├── __init__.py
│   ├── rag_engine.py
│   ├── sentiment.py
│   ├── translator.py
│   ├── image_handler.py
│   └── updater.py
│
├── data
│   ├── medquad.csv
│   ├── arxiv_subset.csv
│   ├── intents.json
│   └── knowledge.txt
│
├── scripts
│   └── build_faiss_index.py
│
├── storage
│   ├── faiss_index
│   └── vector_db
│
├── uploads
├── tests
│
├── main.py
├── config.py
├── requirements.txt
├── .env.example
└── README.md
```

---

# API Endpoints

| Method | Endpoint              | Description          |
| ------ | --------------------- | -------------------- |
| GET    | `/`                   | Health check         |
| POST   | `/chat`               | Chat endpoint        |
| POST   | `/vision`             | Image analysis       |
| POST   | `/voice/transcribe`   | Voice transcription  |
| GET    | `/knowledge/stats`    | Knowledge statistics |
| POST   | `/knowledge/url`      | Add URL              |
| POST   | `/knowledge/text`     | Add text             |
| POST   | `/knowledge/file`     | Add file or PDF      |
| DELETE | `/knowledge/clear`    | Clear knowledge base |
| GET    | `/analytics`          | Analytics data       |
| GET    | `/settings/languages` | Supported languages  |

---

# Environment Variables

Create a `.env` file inside the backend directory.

```env
GROQ_API_KEY=your_groq_api_key_here

MODEL_NAME=llama-3.3-70b-versatile

VISION_MODEL_PRIMARY=meta-llama/llama-4-scout-17b-16e-instruct

VISION_MODEL_FALLBACK=meta-llama/llama-4-maverick-17b-128e-instruct

EMBEDDING_MODEL=all-MiniLM-L6-v2

FAISS_INDEX_PATH=storage/faiss_index

FRONTEND_URL=http://localhost:3000
```

---

# Installation

Navigate to the backend directory:

```bash
cd backend
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the Backend

Start the development server:

```bash
python -m uvicorn main:app --port 8000
```

For LAN/mobile testing:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

# Knowledge Base Construction

## Step 1: Prepare Datasets

Place datasets inside:

```text
backend/data
```

Files:

```text
medquad.csv
arxiv_subset.csv
knowledge.txt
```

---

## Step 2: Build FAISS Index

Run:

```bash
python scripts\build_faiss_index.py
```

Generated files:

```text
backend/storage/faiss_index/index.faiss

backend/storage/faiss_index/documents.pkl
```

---

# Dataset Statistics

```text
Medical Q&A Documents      : 16,359
Research Papers            : 355
Custom Knowledge Documents : 1
------------------------------------------------
Total Indexed Documents    : 16,715
```

---

# Backend Responsibilities

The backend manages:

* Groq API communication
* Prompt generation
* Retrieval-Augmented Generation
* FAISS search
* Image processing
* Voice transcription
* Sentiment analysis
* Translation
* Knowledge management
* PDF ingestion
* API responses

---

# Future Improvements

Potential backend enhancements include:

* User authentication
* Database integration
* Chat history persistence
* Incremental indexing
* Advanced medical NLP
* Citation ranking
* Web search integration
* Tool calling support
* Docker deployment
* Monitoring and logging systems

---

# Author

**Vinayak Varshith Reddy Vangeti**
AI/ML Intern
Elevance Skills Internship

Email: [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com)

Project: waterGPT — Multi-Modal, Multilingual RAG Chatbot

---

# Disclaimer

The medical assistant is intended solely for educational and informational purposes.

It should not be considered a substitute for professional medical advice, diagnosis, or treatment. Always consult qualified healthcare professionals regarding medical concerns.
