# waterGPT: Multi-Modal, Multilingual RAG Chatbot

waterGPT is a full-stack AI chatbot developed as part of the Elevance Skills Internship. The project combines medical question answering, scientific research assistance (with paper search, extractive summarization, and concept visualization), multi-modal image understanding and generation via Google Gemini, sentiment analysis, multilingual communication, voice transcription, and Retrieval-Augmented Generation (RAG) into a single intelligent platform.

The system integrates multiple AI technologies including Large Language Models, Google Gemini multi-modal models, Vector Databases, Semantic Search, Classical NLP (TF-IDF, TextRank), Voice Processing, and Dynamic Knowledge Base Expansion. It demonstrates how modern AI applications can combine multiple capabilities into a unified and scalable solution.

The repository includes:

- Streamlit Interface — Primary Internship-Compatible Implementation
- Next.js + FastAPI Interface — Advanced Production-Style Implementation

The Streamlit interface satisfies all internship requirements, while the Next.js + FastAPI implementation extends the project into a more realistic production-ready architecture.

---

# Author

**Name:** Vinayak Varshith Reddy Vangeti

**Role:** AI/ML Intern

**Program:** Elevance Skills Internship

**Email:** varshithreddyy6@gmail.com

---

# Project Motivation

Artificial Intelligence chatbots have become increasingly powerful; however, many systems still suffer from limitations such as hallucinations, lack of domain-specific knowledge, inability to process multiple modalities, and poor multilingual support.

In domains such as healthcare and scientific research, incorrect information can reduce trust and usefulness. Traditional chatbots often generate answers solely from model knowledge without referencing external data sources.

waterGPT was developed to address these challenges through the integration of:

- Retrieval-Augmented Generation (RAG)
- Domain-specific knowledge bases
- Semantic search
- Multi-modal image understanding and generation
- Research paper search and extractive summarization
- Sentiment-aware interaction
- Multilingual communication
- Dynamic knowledge updates

The project demonstrates how modern AI systems can provide more reliable and contextual responses by combining Large Language Models with external knowledge retrieval.

---

# Project Overview

waterGPT is designed as an intelligent assistant capable of answering questions across multiple domains while maintaining contextual awareness and supporting real-time knowledge expansion.

The platform can:

- Answer general user questions
- Retrieve medical information from MedQuAD
- Search, summarize, and visualize arXiv research papers
- Analyze uploaded images
- Generate new images
- Edit existing images
- Detect user sentiment
- Support multilingual interaction
- Accept voice input
- Expand its knowledge base dynamically
- Provide source-aware responses

Unlike conventional chatbots, waterGPT retrieves relevant information from indexed knowledge sources before generating responses. This retrieval-first approach improves factual accuracy and reduces hallucinations.

The system uses:

- Groq-hosted Llama Models
- Google Gemini Multi-Modal Models (image understanding, image generation, image editing)
- FAISS Vector Database
- SentenceTransformers Embeddings
- TF-IDF + TextRank Extractive Summarization (scikit-learn)
- VADER Sentiment Analysis
- Translation Services
- Voice Transcription Models

---

# Objectives

The primary objectives of waterGPT are:

## 1. Intelligent Question Answering

Develop a chatbot capable of answering questions across multiple domains while maintaining contextual relevance and response quality.

## 2. Medical Knowledge Retrieval

Build a medical assistant using trusted medical question-answer datasets and retrieval-based response generation.

## 3. Research Assistance

Enable users to explore scientific topics using information retrieved from real research papers, with dedicated paper search, extractive summarization, keyword extraction, and concept visualization.

## 4. Multi-Modal Interaction

Support bidirectional image-based interaction: understanding uploaded images, generating brand-new images from text prompts, and editing existing images via text instructions, using Google Gemini.

## 5. Dynamic Knowledge Expansion

Allow users to continuously expand the chatbot's knowledge through external sources.

## 6. Multilingual Communication

Provide seamless interaction across multiple languages.

## 7. Sentiment-Aware Responses

Adapt responses based on detected user sentiment.

## 8. Voice Interaction

Enable speech-based interaction through audio transcription.

# Internship Tasks Covered

The project successfully implements all internship requirements.

| Internship Task | Implementation |
|-----------------|----------------|
| Dynamic Knowledge Base Expansion | URL, text, file, and PDF ingestion with automatic FAISS updates |
| Multi-Modal Chatbot (Google Gemini) | Image understanding, image generation, and image editing using Google Gemini (gemini-2.5-flash, gemini-2.5-flash-image) |
| Medical Q&A Chatbot using MedQuAD | RAG-based medical assistant using MedQuAD |
| arXiv Research Expert Chatbot | Dedicated paper search (keyword/category/author filters), TextRank extractive summarization, TF-IDF keyword extraction, and TF-IDF + SVD concept-map visualization, in addition to conversational retrieval |
| Sentiment Analysis | VADER-based sentiment classification |
| Multilingual Chatbot | Language detection and translation support |

---

# Core Features

## General Chat Assistant

The chatbot supports natural conversation using Groq-hosted Llama models.

### Features

- Context-aware responses
- Follow-up question handling
- Multi-turn conversations
- Semantic understanding
- Response generation using LLMs

---

## Medical Assistant

The medical assistant retrieves information from the MedQuAD dataset before generating responses.

### Capabilities

- Medical question answering
- Medical knowledge retrieval
- Symptom explanation
- Disease information retrieval
- Treatment-related information
- Educational medical responses

### Additional Functionality

- Medical entity recognition
- Retrieval-based grounding
- Safety reminders

> **Note:** The assistant is intended for educational purposes and does not replace professional medical advice.

---

## Research Assistant

The research assistant uses arXiv research papers to answer scientific and technical questions. It also provides a dedicated research toolkit including paper search, extractive summarization, keyword extraction, and concept visualization.

The Research Assistant is organized into three modes.

### 1. Ask (Conversational RAG)

- Research paper retrieval via FAISS
- Scientific concept explanation
- Research-oriented discussions
- Technical knowledge exploration

### 2. Search Papers

A dedicated structured search interface over the indexed arXiv corpus.

Features include:

- Free-text search across paper titles and abstracts
- Filter by arXiv category (cs.AI, cs.CL, cs.LG, cs.IR, cs.CV)
- Filter by author name
- Per-paper **Summarize + Keywords** action using TextRank and TF-IDF

### 3. Visualize

Concept visualization computed directly from the indexed arXiv corpus.

Includes:

- Category distribution bar chart
- Corpus keyword frequency using TF-IDF
- Concept map generated using TF-IDF + Truncated SVD

### Summarization & Information Extraction

Paper summaries are generated using **TextRank**, a graph-based extractive summarization algorithm built on TF-IDF sentence similarity.

Keyword extraction uses **TF-IDF scoring** over n-grams.

Both methods execute locally using **scikit-learn**, without requiring an LLM.

### Supported Domains

- Artificial Intelligence
- Machine Learning
- Natural Language Processing
- Information Retrieval
- Computer Vision

---

## Vision AI (Google Gemini)

The Vision AI module is powered by Google Gemini and supports a complete bidirectional multi-modal workflow.

### 1. Understand (Image → Text)

Features:

- Image upload
- Visual question answering
- Object understanding
- Visual reasoning
- Context-aware image explanations

Powered by:

- gemini-2.5-flash

Example prompts:

- Describe this image.
- What objects are visible?
- Explain what is happening in this image.
- Identify important visual elements.

---

### 2. Generate (Text → Image)

Features:

- Generate brand-new images from text prompts
- Images rendered directly in the chat interface

Powered by:

- gemini-2.5-flash-image

Example prompt:

> A watercolor painting of a mountain lake at sunset.

---

### 3. Edit (Image + Text → Image)

Features:

- Upload an existing image
- Describe required modifications
- Receive a newly generated edited image

Powered by:

- gemini-2.5-flash-image

Example prompt:

> Turn this image into a watercolor painting.

This completes the internship requirement for a Multi-Modal Chatbot by supporting image understanding, image generation, and image editing.

---

# Voice Input

The advanced interface supports voice-based interaction.

## Features

- Browser audio recording
- Audio upload
- Speech-to-text conversion
- Automatic transcription
- Chat integration

Voice processing is handled using **Groq Whisper** transcription models.

---

# Dynamic Knowledge Base Expansion

One of the most important features of waterGPT is the ability to continuously expand its knowledge base.

## Supported Sources

- URLs
- Plain Text
- Text Files
- CSV Files
- Markdown Files
- PDF Documents

The uploaded content is automatically:

- Extracted
- Cleaned
- Chunked
- Embedded
- Indexed into FAISS

Once indexed, the content becomes available for future retrieval.

---

# Sentiment Analysis

The system performs sentiment analysis on user messages.

## Supported Sentiment Categories

- Positive
- Neutral
- Negative

Sentiment information can be used to:

- Analyze conversations
- Track interaction patterns
- Adjust response tone
- Generate analytics data

---

# Multilingual Support

waterGPT supports multilingual communication through automatic language detection and translation.

## Workflow

1. Language Detection
2. Translation to English
3. Knowledge Retrieval
4. Response Generation
5. Translation Back to Target Language

The system supports **30+ languages**, including:

- English
- Hindi
- Telugu
- Tamil
- Spanish
- French
- German
- Arabic
- Chinese
- Japanese
- Portuguese
- Russian
- Korean

and many more.

---

# System Architecture

waterGPT follows a modular architecture that combines user interaction, knowledge retrieval, AI reasoning, image understanding, sentiment analysis, translation, and dynamic knowledge expansion.

The architecture separates responsibilities across the frontend, backend, AI services, and data storage components.

```text
User
 |
 v
Streamlit Interface / Next.js Frontend
 |
 v
FastAPI Backend
 |
 +--------------------+--------------------+
 |                    |                    |
 v                    v                    v
RAG Engine      Vision Service      Research Engine
 |                    |                    |
 v                    v                    v
FAISS Vector DB   Google Gemini      TF-IDF / TextRank /
 |               (Understand /       Truncated SVD
 v                Generate / Edit)         |
Knowledge Sources                          v
 |                                  Search · Summarize ·
 +--------------------------+       Keyword Extraction ·
 |            |             |       Concept Map
 v            v             v
MedQuAD    arXiv      User Knowledge
```

The architecture allows each module to operate independently while sharing common retrieval and response-generation infrastructure.

---

# Architecture Components

## Frontend Layer

The frontend is responsible for collecting user input and displaying chatbot responses.

### Streamlit Interface

Primary internship-compatible implementation.

**Features**

- Simple chatbot interface
- Medical assistant
- Research assistant
- Vision AI
- Knowledge base management
- Sentiment analytics
- Language settings

### Next.js Interface

Advanced production-ready frontend.

**Features**

- Responsive UI
- Multi-page navigation
- Voice input
- Better source visualization
- Mobile support
- Analytics dashboard
- Enhanced user interactions

---

## Backend Layer

The FastAPI backend serves as the central processing layer.

### Responsibilities

- Request handling
- AI model communication
- Retrieval operations
- Knowledge management
- Translation
- Sentiment analysis
- Image processing
- Voice transcription

The backend exposes REST APIs consumed by both frontend implementations.

---

## AI Layer

The AI layer contains multiple specialized models.

### Text Generation Models

Used for:

- General conversation
- Medical responses
- Research explanations
- Knowledge-grounded answers

### Vision Models

Used for:

- Image understanding
- Visual question answering
- Object recognition
- Image explanation

### Voice Models

Used for:

- Audio transcription
- Speech-to-text conversion

---

## Knowledge Layer

The knowledge layer stores indexed information that can be retrieved during conversations.

### Sources

- Medical datasets
- Research papers
- User-added knowledge
- Uploaded files
- External URLs

This layer is implemented using the **FAISS Vector Database**.

---

# End-to-End Workflow

```text
User Query
    |
    v
Language Detection
    |
    v
Translation (if required)
    |
    v
Embedding Generation
    |
    v
FAISS Similarity Search
    |
    v
Relevant Context Retrieval
    |
    v
Prompt Construction
    |
    v
Groq Llama Model
    |
    v
Response Generation
    |
    v
Translation (if required)
    |
    v
User Response
```

This workflow ensures that generated responses are grounded in retrieved information whenever relevant knowledge is available.

# Retrieval-Augmented Generation (RAG) Pipeline

waterGPT follows a Retrieval-Augmented Generation (RAG) architecture.

Instead of relying entirely on the model's internal knowledge, the chatbot retrieves relevant information from external knowledge sources before generating a response.

The RAG pipeline consists of the following stages.

---

## Stage 1: Document Collection

Knowledge is collected from multiple sources.

### Sources

- MedQuAD
- arXiv Research Papers
- Text Files
- PDF Documents
- URLs
- User Documents

---

## Stage 2: Text Extraction

Raw content is extracted from each source.

### PDF

```text
PDF File
      ↓
Text Extraction
      ↓
Plain Text
```

### URL

```text
Web Page
      ↓
HTML Parsing
      ↓
Clean Text
```

### CSV

```text
CSV File
      ↓
Structured Records
      ↓
Text Documents
```

---

## Stage 3: Chunking

Large documents are divided into smaller chunks before embedding.

### Benefits

- Improved retrieval accuracy
- Better embedding quality
- Reduced context size
- Faster similarity search

### Example

```text
Document
 |
 +-- Chunk 1
 +-- Chunk 2
 +-- Chunk 3
 +-- Chunk 4
```

---

## Stage 4: Embedding Generation

Each document chunk is converted into a dense vector representation.

### Embedding Model

```text
all-MiniLM-L6-v2
```

### Characteristics

- Lightweight
- Fast
- Semantic understanding
- 384-dimensional embeddings

---

## Stage 5: FAISS Indexing

Embeddings are stored inside a FAISS vector database.

### Benefits

- Fast retrieval
- Efficient similarity search
- Scalable architecture
- Low memory usage

### Stored Files

```text
backend/storage/faiss_index/index.faiss

backend/storage/faiss_index/documents.pkl
```

---

## Stage 6: Query Embedding

When a user asks a question:

```text
User Query
      ↓
Embedding Generation
      ↓
Query Vector
```

The query is converted into the same embedding space as the indexed documents.

---

## Stage 7: Similarity Search

FAISS performs nearest-neighbor search.

```text
User Query
      ↓
FAISS Search
      ↓
Top Relevant Chunks
```

Only the most relevant document chunks are selected.

---

## Stage 8: Context Injection

Retrieved chunks are injected into the prompt before it is sent to the language model.

### Example

```text
System Prompt
      +
Retrieved Context
      +
User Question
```

This gives the language model relevant external knowledge before generating a response.

---

## Stage 9: Response Generation

The LLM receives:

- User Question
- Retrieved Context
- System Instructions

It then generates a grounded and context-aware response.

---

# Dataset Description

waterGPT combines multiple datasets into a unified knowledge base.

---

## MedQuAD Dataset

### Source

https://github.com/abachaa/MedQuAD

### Purpose

- Medical Question Answering
- Healthcare Information Retrieval

### Characteristics

- Trusted medical sources
- Question-answer pairs
- Educational medical content

### Used For

- Symptoms
- Diseases
- Treatments
- Medical procedures
- Healthcare information

### Indexed Documents

```text
16,359
```

---

## arXiv Dataset

### Source

https://arxiv.org/help/api

### Purpose

Research Assistance

### Categories

```text
cs.AI
cs.CL
cs.LG
cs.IR
cs.CV
```

### Contains

- Research paper titles
- Authors
- Categories
- Abstracts

### Indexed Documents

```text
355
```

---

## Custom Knowledge Dataset

Purpose:

- Project-specific knowledge
- System information
- Additional contextual data

### Indexed Documents

```text
1
```

---

# Dataset Statistics

| Dataset | Documents |
|----------|----------:|
| MedQuAD Medical Q&A | 16,359 |
| arXiv Research Papers | 355 |
| Custom Knowledge | 1 |
| **Total Indexed Documents** | **16,715** |

All documents are converted into embeddings and stored inside the FAISS vector database.

# Technology Stack

## Frontend Technologies

- Next.js
- React
- JavaScript
- CSS
- Recharts
- Marked

---

## Backend Technologies

- Python
- FastAPI
- Groq API
- Google Gemini API (google-genai)
- FAISS
- SentenceTransformers
- scikit-learn (TF-IDF, TextRank, Truncated SVD)
- Pillow
- BeautifulSoup
- Feedparser
- Langdetect
- Deep Translator
- PyPDF

---

## AI Technologies

### Text Generation

```text
Groq Llama Models
```

Used for:

- General chat
- Medical responses
- Research explanations
- Knowledge-grounded answers

---

### Multi-Modal Vision

```text
Google Gemini
(gemini-2.5-flash, gemini-2.5-flash-image)
```

Used for:

- Image understanding
- Visual question answering
- Text-to-image generation
- Image editing using text prompts

---

### Voice Transcription

```text
Groq Whisper
```

Used for:

- Speech-to-text conversion
- Voice chat support

---

### Embeddings

```text
all-MiniLM-L6-v2
```

Used for:

- Semantic search
- Document retrieval
- Similarity matching

---

### Vector Database

```text
FAISS
```

Used for:

- Embedding storage
- Fast similarity search
- Retrieval operations

---

### Extractive Summarization & Information Extraction

```text
TF-IDF + TextRank (scikit-learn)
```

Used for:

- Extractive summarization
- Keyword extraction
- Corpus keyword frequency analysis
- Concept-map visualization using Truncated SVD

---

# Backend Components

The backend follows a modular service-oriented architecture where each service is responsible for a specific functionality.

---

## Chat Service

**File**

```text
services/chat_service.py
```

### Responsibilities

- General conversation
- Prompt construction
- Response generation
- Context injection
- Chat orchestration

This service acts as the primary interaction layer between users and the AI models.

---

## Vision Service

**File**

```text
services/vision_service.py
```

### Responsibilities

- Image processing
- Google Gemini communication
- Image understanding
- Image generation
- Image editing
- Visual question answering

Supported operations:

- `analyze_image()`
- `generate_image_from_text()`
- `edit_image_with_text()`

---

## Research Service

**File**

```text
utils/research_engine.py
```

### Responsibilities

- Structured arXiv paper search
- TextRank summarization
- TF-IDF keyword extraction
- Keyword frequency analysis
- TF-IDF + Truncated SVD concept-map generation

Exposed through:

```text
api/research.py
```

---

## Knowledge Service

**File**

```text
services/knowledge_service.py
```

### Responsibilities

- Knowledge ingestion
- Document chunking
- Embedding generation
- FAISS indexing
- Retrieval operations

This service powers the Retrieval-Augmented Generation (RAG) pipeline.

---

## Analytics Service

**File**

```text
services/analytics_service.py
```

### Responsibilities

- Sentiment statistics
- Analytics reporting
- Dashboard support

---

## Settings Service

**File**

```text
services/settings_service.py
```

### Responsibilities

- Language settings
- Configuration management
- Frontend settings

---

## Medical NER Service

**File**

```text
services/medical_ner_service.py
```

### Responsibilities

- Symptom extraction
- Disease detection
- Treatment identification
- Medical entity recognition

Provides domain-specific medical understanding.

---

# Backend API Endpoints

The FastAPI backend exposes REST APIs used by both frontend implementations.

---

## Health Check

**Endpoint**

```http
GET /
```

**Purpose**

Verifies that the backend is running correctly.

---

## Chat Endpoint

**Endpoint**

```http
POST /chat
```

**Purpose**

- General chat
- Medical chat
- Research chat

**Response**

Generated AI response with optional source information.

---

## Vision Endpoint

**Endpoint**

```http
POST /vision
```

**Purpose**

Handles image uploads and visual question answering using Google Gemini.

---

## Image Generation Endpoint

**Endpoint**

```http
POST /vision/generate
```

**Purpose**

Generates brand-new images from text prompts.

**Response**

```json
{
  "caption": "...",
  "image_url": "..."
}
```

---

## Image Editing Endpoint

**Endpoint**

```http
POST /vision/edit
```

**Purpose**

Edits uploaded images using text instructions.

**Response**

```json
{
  "caption": "...",
  "image_url": "..."
}
```

---

## Generated Image Retrieval

**Endpoint**

```http
GET /vision/generated/{filename}
```

Returns previously generated images.

---

## Voice Transcription

**Endpoint**

```http
POST /voice/transcribe
```

Converts audio into text using Groq Whisper.

---

## Knowledge Statistics

**Endpoint**

```http
GET /knowledge/stats
```

Returns indexed document statistics.

---

## Add Knowledge from URL

**Endpoint**

```http
POST /knowledge/url
```

Adds website content into the knowledge base.

---

## Add Knowledge from Text

**Endpoint**

```http
POST /knowledge/text
```

Adds plain text into the knowledge base.

---

## Add Knowledge from File

**Endpoint**

```http
POST /knowledge/file
```

Supports:

- TXT
- CSV
- Markdown
- PDF

Uploaded files are automatically indexed into FAISS.

---

## Clear Knowledge Base

**Endpoint**

```http
DELETE /knowledge/clear
```

Removes all dynamically added knowledge.

---

## Supported Languages

**Endpoint**

```http
GET /settings/languages
```

Returns all available language options.

# Frontend Pages

The advanced Next.js frontend contains multiple pages designed around specific chatbot capabilities.

---

## Home Page

**Route**

```text
/
```

### Purpose

- Landing page
- Project introduction
- Navigation to all chatbot modules

---

## Chat Page

**Route**

```text
/chat
```

### Purpose

- General AI conversations
- Multi-turn dialogue
- Voice-enabled chat

---

## Medical Assistant

**Route**

```text
/medical
```

### Purpose

- Medical question answering
- Healthcare information retrieval
- Educational medical assistance

---

## Research Assistant

**Route**

```text
/research
```

### Purpose

- Conversational research assistant
- Scientific paper retrieval
- arXiv paper search
- Paper summarization
- Keyword extraction
- Category visualization
- Concept-map visualization

---

## Vision AI

**Route**

```text
/vision
```

### Purpose

- Image upload
- Image understanding
- Visual question answering
- Text-to-image generation
- Image editing

---

## Knowledge Base Manager

**Route**

```text
/knowledge
```

### Purpose

- Add URLs
- Add text
- Upload documents
- Upload PDFs
- Manage indexed knowledge

---

## Language Settings

**Route**

```text
/language
```

### Purpose

- Language selection
- Translation configuration

---

## Analytics Dashboard

**Route**

```text
/analytics
```

### Purpose

- Sentiment analytics
- Usage statistics
- System analytics

---

## Settings Page

**Route**

```text
/settings
```

### Purpose

- Application configuration
- System settings

---

# Project Structure

```text
Elevance_Skills_Internship
│
├── backend
│   ├── api
│   ├── core
│   ├── data
│   ├── schemas
│   ├── scripts
│   ├── services
│   ├── storage
│   ├── tests
│   ├── uploads
│   ├── utils
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend
│   ├── app
│   ├── components
│   ├── hooks
│   ├── lib
│   ├── public
│   ├── styles
│   ├── package.json
│   └── .env.example
│
├── legacy_streamlit
│   └── app.py
│
├── notebooks
├── reports
├── screenshots
├── README.md
└── .gitignore
```

---

# Installation Guide

Before running the project, ensure the following software is installed.

## Prerequisites

- Python 3.10+
- Node.js 18+
- npm
- Git

---

# Backend Setup

Navigate to the backend directory.

```bash
cd backend
```

Create a virtual environment.

```bash
python -m venv venv
```

Activate the virtual environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies.

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file inside the **backend** directory.

```env
GROQ_API_KEY=your_groq_api_key_here

MODEL_NAME=llama-3.3-70b-versatile

VISION_MODEL_PRIMARY=meta-llama/llama-4-scout-17b-16e-instruct

VISION_MODEL_FALLBACK=meta-llama/llama-4-maverick-17b-128e-instruct

# Google Gemini API
GEMINI_API_KEY=your_gemini_api_key_here

GEMINI_VISION_MODEL=gemini-2.5-flash

GEMINI_IMAGE_MODEL=gemini-2.5-flash-image

EMBEDDING_MODEL=all-MiniLM-L6-v2

FAISS_INDEX_PATH=storage/faiss_index

FRONTEND_URL=http://localhost:3000
```

> **Note:** Gemini's free API tier generally supports text and vision understanding (`gemini-2.5-flash`). Image generation (`gemini-2.5-flash-image`) requires a billing-enabled Google Cloud project.

---

# Running the Backend

Start the backend server.

```bash
python -m uvicorn main:app --port 8000
```

For LAN testing:

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Backend URL:

```text
http://localhost:8000
```

Swagger Documentation:

```text
http://localhost:8000/docs
```

---

# Frontend Setup

Navigate to the frontend directory.

```bash
cd frontend
```

Install dependencies.

```bash
npm install
```

Create a file named:

```text
.env.local
```

Add:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Run the frontend.

```bash
npm run dev
```

For LAN testing.

```bash
npm run dev -- --hostname 0.0.0.0
```

Frontend URL:

```text
http://localhost:3000
```

---

# Streamlit Interface

Ensure the backend is already running.

From the project root:

```bash
backend\venv\Scripts\python.exe -m streamlit run legacy_streamlit\app.py
```

Streamlit URL:

```text
http://localhost:8501
```

# Building the Knowledge Base

The knowledge base can be rebuilt using the provided scripts.

---

## 1. Convert MedQuAD Dataset

```bash
cd backend
python scripts\convert_medquad.py
```

---

## 2. Download arXiv Dataset

```bash
python scripts\download_arxiv_subset.py
```

---

## 3. Build FAISS Index

```bash
python scripts\build_faiss_index.py
```

Generated files:

```text
backend/storage/faiss_index/index.faiss

backend/storage/faiss_index/documents.pkl
```

---

# Screenshots

The project includes screenshots demonstrating the functionality of both the Streamlit interface and the advanced Next.js frontend.

Place all screenshots inside the **screenshots** directory.

## Screenshot Structure

```text
screenshots
│
├── home.png
├── chat.png
├── medical.png
├── research.png
├── vision.png
├── knowledge.png
├── analytics.png
├── settings.png
├── streamlit_overview.png
├── streamlit_medical.png
├── mobile_chat.png
├── mobile_vision.png
└── architecture.png
```

---

# Advanced Next.js Interface

## Home Page

Displays the landing page, project overview, and navigation.

```text
screenshots/home.png
```

---

## Chat Interface

General conversational AI interface.

```text
screenshots/chat.png
```

---

## Medical Assistant

Medical question answering using MedQuAD retrieval.

```text
screenshots/medical.png
```

---

## Research Assistant

Research-focused assistant powered by arXiv papers.

```text
screenshots/research.png
```

---

## Vision AI

Image understanding, image generation, and image editing using Google Gemini.

```text
screenshots/vision.png
```

---

## Knowledge Base Manager

Knowledge ingestion and management interface.

```text
screenshots/knowledge.png
```

---

## Analytics Dashboard

Displays sentiment analytics and usage statistics.

```text
screenshots/analytics.png
```

---

## Settings Page

Application configuration and language settings.

```text
screenshots/settings.png
```

---

# Streamlit Interface

## Overview

Primary internship-compatible implementation.

```text
screenshots/streamlit_overview.png
```

---

## Medical Assistant

Medical chatbot implemented using Streamlit.

```text
screenshots/streamlit_medical.png
```

---

# Mobile Responsive Interface

## Mobile Chat

Responsive chatbot interface.

```text
screenshots/mobile_chat.png
```

---

## Mobile Vision

Responsive Vision AI interface.

```text
screenshots/mobile_vision.png
```

---

# Results

The completed system successfully integrates multiple AI technologies into a single platform.

The chatbot supports:

- General conversation
- Medical question answering
- Research assistance
- Image understanding
- Image generation
- Image editing
- Voice interaction
- Sentiment analysis
- Multilingual communication
- Dynamic knowledge expansion
- Retrieval-Augmented Generation (RAG)

---

# Knowledge Base Results

Final indexed knowledge base statistics:

```text
Medical Q&A Documents      : 16,359
Research Papers            : 355
Custom Knowledge Documents : 1
-----------------------------------------------
Total Indexed Documents    : 16,715
```

All documents are converted into vector embeddings and indexed using FAISS.

---

# Functional Results

## General Chat

- Natural conversation
- Context-aware interaction
- Multi-turn dialogue

---

## Medical Assistant

- Medical information retrieval
- Medical question answering
- Medical entity recognition

---

## Research Assistant

- Scientific concept explanation
- Research paper retrieval
- Paper search with filters
- Extractive summarization (TextRank)
- Keyword extraction (TF-IDF)
- Category distribution visualization
- Keyword frequency visualization
- Concept-map visualization

---

## Vision AI

- Image understanding (Google Gemini)
- Text-to-image generation
- Image editing using text prompts
- Context-aware visual interpretation

---

## Voice Interaction

- Audio recording
- Speech transcription
- Voice-enabled conversations

---

## Dynamic Knowledge Base

- URL ingestion
- Text ingestion
- File ingestion
- PDF ingestion
- Real-time FAISS index updates

---

## Multilingual Communication

- Language detection
- Translation
- Cross-language interaction

---

## Sentiment Analysis

- Positive classification
- Neutral classification
- Negative classification

# Example Use Cases

## Medical Question Answering

### User Query

```text
What are the symptoms of diabetes?
```

waterGPT retrieves relevant medical information and generates an educational response covering:

- Increased thirst
- Frequent urination
- Fatigue
- Blurred vision
- Unexplained weight loss

---

## Research Assistant

### User Query

```text
Explain Retrieval-Augmented Generation.
```

waterGPT retrieves relevant research papers and explains:

- Retrieval systems
- Large Language Models
- Context injection
- Knowledge grounding

### Search Papers Example

```text
Query: "retrieval"
Category: "cs.IR"
```

Returns matching arXiv papers with a **Summarize + Keywords** option for each paper, producing:

- TextRank extractive summary
- TF-IDF keywords

No LLM is required for this summarization process.

### Visualization Example

The **Visualize** tab renders:

- Category distribution bar chart
- Top TF-IDF keywords across the corpus
- 2D concept-map scatter plot (TF-IDF + Truncated SVD)

---

## Vision AI

### Understand Example

```text
Upload an image and ask:
"Describe this image."
```

Google Gemini (`gemini-2.5-flash`) analyzes the uploaded image and provides a detailed explanation.

### Generate Example

```text
Prompt:
"A watercolor painting of a mountain lake at sunset"
```

Google Gemini (`gemini-2.5-flash-image`) generates a brand-new image, which is displayed directly in the chat.

### Edit Example

```text
Upload an image and instruct:
"Turn this into a watercolor painting."
```

Google Gemini returns an edited version of the uploaded image.

---

## Voice Interaction

### User Input

```text
What is Machine Learning?
```

The system performs the following steps:

1. Records audio
2. Converts speech to text
3. Processes the query
4. Generates an AI response

---

# Performance Summary

The project successfully integrates:

- Large Language Models
- Vision Models
- Voice Models
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- Translation Services
- Sentiment Analysis

The modular architecture supports scalability and future feature expansion.

---

# Challenges Faced

## 1. Large Dataset Processing

The MedQuAD dataset contains thousands of medical documents that require efficient preprocessing and indexing.

### Challenges

- Data cleaning
- Data conversion
- Embedding generation
- FAISS index creation

---

## 2. Retrieval Quality

Maintaining retrieval accuracy across multiple domains required careful experimentation.

### Challenges

- Semantic search quality
- Chunk sizing
- Context relevance

---

## 3. Multi-Domain Knowledge

The chatbot combines:

- Medical knowledge
- Research knowledge
- User-generated knowledge

Balancing retrieval quality across these domains required additional tuning.

---

## 4. Multilingual Processing

Supporting multiple languages introduced challenges related to:

- Translation quality
- Language detection
- Response consistency

---

## 5. Vision Integration

Image processing required:

- Image encoding
- Google Gemini API integration
- Prompt engineering
- Image storage and retrieval
- Billing-aware image generation workflow

---

## 6. Voice Processing

Voice transcription required:

- Browser compatibility
- Audio conversion
- Speech recognition integration

---

## 7. Responsive Frontend Design

Developing a consistent experience across:

- Desktop
- Tablet
- Mobile

required extensive UI optimization.

---

# Learning Outcomes

This project provided practical experience in several AI and software engineering domains.

## Artificial Intelligence

- Large Language Models
- Vision Models
- Prompt Engineering
- Multi-modal AI
- AI Application Design

---

## Natural Language Processing

- Semantic Search
- Language Detection
- Translation Systems
- Sentiment Analysis
- Medical NLP

---

## Retrieval-Augmented Generation

- Document Processing
- Text Chunking
- Embedding Generation
- Vector Databases
- Context Retrieval

---

## Backend Development

- FastAPI
- REST APIs
- Service-Oriented Architecture
- Data Processing Pipelines

---

## Frontend Development

- Next.js
- React
- Responsive Design
- State Management
- API Integration

---

## Data Engineering

- Dataset Preparation
- Data Cleaning
- FAISS Index Construction
- Knowledge Management

# Future Improvements

Several enhancements can further improve the project.

---

## AI Improvements

- Tool calling support
- Web search integration
- Advanced reasoning workflows
- Multi-turn conversational image editing (iterative refinement)

---

## Medical Improvements

- Biomedical Named Entity Recognition (NER) models
- Drug interaction analysis
- Expanded medical knowledge base

---

## Research Improvements

- Additional arXiv categories
- Research paper recommendations
- Citation extraction
- Abstractive (LLM-assisted) summarization alongside TextRank
- Interactive concept-map filtering by category

---

## Knowledge Base Improvements

- Incremental indexing
- Document versioning
- Advanced search filters

---

## User Experience Improvements

- User authentication
- User profiles
- Chat history storage
- Theme customization

---

## Deployment Improvements

- Cloud deployment
- Docker support
- CI/CD pipelines
- Monitoring dashboards

---

# Evaluation Highlights

This project demonstrates:

- Full-stack AI development
- Retrieval-Augmented Generation (RAG)
- Multi-modal AI integration
- Medical AI applications
- Research assistance systems
- Voice-enabled AI interaction
- Multilingual chatbot design
- Dynamic knowledge management
- Modern frontend development
- Production-style backend architecture

---

# References

## Datasets

### MedQuAD

https://github.com/abachaa/MedQuAD

### arXiv API

https://arxiv.org/help/api

---

## Libraries and Frameworks

### FastAPI

https://fastapi.tiangolo.com

### Next.js

https://nextjs.org

### FAISS

https://github.com/facebookresearch/faiss

### SentenceTransformers

https://www.sbert.net

### Groq

https://groq.com

### Google Gemini API

https://ai.google.dev/gemini-api/docs

### scikit-learn

https://scikit-learn.org

---

# Conclusion

waterGPT demonstrates the successful integration of Retrieval-Augmented Generation (RAG), Medical Question Answering, arXiv Research Assistance (search, extractive summarization, and concept visualization), Google Gemini-powered Multi-Modal Interaction (image understanding, generation, and editing), Voice Processing, Sentiment Analysis, and Multilingual Communication within a unified AI platform.

The project fulfills all internship requirements while extending beyond them through:

- A production-style Next.js frontend
- A modular FastAPI backend
- Standalone NLP techniques (TF-IDF, TextRank, Truncated SVD)
- Bidirectional multi-modal AI using Google Gemini
- A scalable Retrieval-Augmented Generation pipeline powered by FAISS

The final system combines modern AI techniques with sound software engineering principles, providing a strong foundation for future research, development, and real-world deployment.

---

# Author

**Vinayak Varshith Reddy Vangeti**

AI/ML Intern

Elevance Skills Internship

**Email:** varshithreddyy6@gmail.com

**Project:** waterGPT — Multi-Modal, Multilingual RAG Chatbot

---

# Disclaimer

The medical assistant included in this project is intended solely for educational and informational purposes.

It should **not** be considered a substitute for professional medical advice, diagnosis, or treatment.

Users should always consult qualified healthcare professionals regarding medical concerns before making medical decisions.

