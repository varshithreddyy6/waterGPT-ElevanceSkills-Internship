# waterGPT Project Report

## Title

**waterGPT: A Multi-Modal, Multilingual RAG Chatbot for Medical and Scientific Question Answering**

---

## Author

**Name:** Vinayak Varshith Reddy Vangeti  
**Email:** [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com)  
**Role:** AI/ML Intern  
**Program:** Elevance Skills Internship  

---

## Abstract

waterGPT is an AI-powered chatbot system developed as part of the Elevance Skills Internship program. The project integrates six major internship tasks into one unified chatbot platform: dynamic knowledge base expansion, multi-modal image understanding, medical question answering using MedQuAD, research assistance using arXiv papers, sentiment analysis, and multilingual support.

The primary internship-compatible implementation is built using Streamlit. An additional advanced production-style interface is implemented using Next.js and FastAPI. The backend uses Groq-hosted open-source Llama models, FAISS vector search, SentenceTransformers embeddings, VADER sentiment analysis, and translation tools.

The final system indexes 16,715 documents, including 16,359 MedQuAD medical Q&A documents, 355 arXiv research papers, and one custom knowledge document. The chatbot can retrieve relevant context, generate grounded responses, analyze images, detect sentiment, support multiple languages, and dynamically expand its knowledge base.

---

## 1. Introduction

Artificial intelligence chatbots have evolved from simple rule-based systems into intelligent assistants capable of understanding natural language, retrieving information, processing images, and generating context-aware responses. In this project, waterGPT was developed as a multi-modal and multilingual chatbot that combines large language models with retrieval-augmented generation.

The project was built as part of the Elevance Skills Internship program and extends the original training chatbot into a complete AI assistant. The final implementation includes both a Streamlit interface for internship compatibility and a Next.js + FastAPI interface as an advanced extension.

---

## 2. Problem Statement

The objective of this project is to build an intelligent chatbot that can answer user questions across multiple domains while supporting real-time knowledge updates, medical Q&A, scientific research explanations, image understanding, sentiment-aware responses, and multilingual interaction.

The chatbot should be able to:

- Retrieve relevant information from a vector database
- Answer medical questions using MedQuAD
- Explain scientific concepts using arXiv research papers
- Understand image inputs
- Detect user emotions through sentiment analysis
- Support multiple languages
- Dynamically expand its knowledge base through user-provided sources
- Provide a simple Streamlit interface for asking questions

---

## 3. Internship Tasks Mapping

| Internship Task | waterGPT Implementation |
|---|---|
| Dynamic knowledge base expansion | URL, text, file, and PDF ingestion with FAISS vector database updates |
| Multi-modal chatbot | Image upload and visual question answering using Groq vision models |
| Medical Q&A chatbot using MedQuAD | RAG-based medical chatbot using 16,359 MedQuAD Q&A documents |
| arXiv research expert chatbot | Research assistant using 355 real arXiv papers fetched through arXiv API |
| Sentiment analysis | VADER-based positive, neutral, and negative sentiment detection |
| Multilingual support | Language detection and translation for multiple languages |

---

## 4. Interfaces Included

This project includes two user interfaces.

### 4.1 Streamlit Interface — Primary Internship Submission

The Streamlit application is included as the primary internship-compatible interface. It implements all required tasks and connects to the same FastAPI backend used by the advanced interface.

The Streamlit interface includes:

- General chat
- Medical Q&A
- Research assistant
- Vision AI
- Knowledge base management
- Sentiment analytics
- Language settings

### 4.2 Next.js + FastAPI Interface — Advanced Extension

The Next.js frontend and FastAPI backend provide a production-style enhanced user experience with a custom UI, mobile support, voice input, advanced source viewing, and chat actions.

The advanced frontend includes:

- Luxury black waterGPT UI
- Mobile responsive interface
- Copy, edit, share, and feedback actions
- Suggested prompt cards
- Chat export
- Better source viewer
- Vision chat
- Knowledge base manager
- Analytics dashboard

---

## 5. Dataset Description

### 5.1 MedQuAD Dataset

**Source:** [https://github.com/abachaa/MedQuAD](https://github.com/abachaa/MedQuAD)

The MedQuAD dataset contains medical question-answer pairs collected from trusted medical sources. It is used to build the medical question-answering module.

The dataset was converted into CSV format and indexed into FAISS.

Final indexed count:

```text
16,359 medical Q&A documents
```

### 5.2 arXiv Dataset

**Source:** [https://arxiv.org/help/api](https://arxiv.org/help/api)

A subset of arXiv papers was collected using the arXiv API from selected computer science categories:

- cs.AI
- cs.CL
- cs.LG
- cs.IR
- cs.CV

The arXiv subset is used by the research assistant module to explain scientific concepts and summarize research-related topics.

Final indexed count:

```text
355 research papers
```

### 5.3 Custom Knowledge File

A project-specific `knowledge.txt` file is included for general project and system knowledge.

Final indexed count:

```text
1 custom knowledge chunk
```

### 5.4 Final Knowledge Base Statistics

```text
Total indexed documents: 16,715
Medical Q&A documents: 16,359
Research papers: 355
Custom knowledge chunks: 1
```

---

## 6. Methodology

### 6.1 Data Collection

The project uses multiple data sources:

1. MedQuAD medical Q&A dataset
2. arXiv research paper data from arXiv API
3. Custom project knowledge file
4. User-added knowledge through URL, text, file, and PDF uploads

### 6.2 Data Preprocessing

The datasets were cleaned and converted into structured text documents.

For MedQuAD, question-answer pairs were formatted as:

```text
Medical Question: ...
Medical Answer: ...
```

For arXiv papers, each document includes:

```text
Research Paper Title
Authors
Categories
Abstract
```

For uploaded text, files, and URLs, the content is chunked into smaller segments suitable for embedding.

### 6.3 Text Chunking

Long text documents are split into chunks to improve retrieval accuracy. The chunking process ensures that each chunk contains enough context while remaining small enough for efficient embedding and search.

### 6.4 Embedding Generation

Text chunks are converted into dense vector embeddings using the SentenceTransformers model:

```text
all-MiniLM-L6-v2
```

This model creates 384-dimensional embeddings suitable for semantic search.

### 6.5 Vector Database

The embeddings are stored in a FAISS vector database. FAISS enables fast similarity search over dense vectors.

The FAISS index files are:

```text
backend/storage/faiss_index/index.faiss
backend/storage/faiss_index/documents.pkl
```
### 6.6 Retrieval-Augmented Generation

When a user asks a question:

1. The query is translated to English if needed.
2. The query is embedded.
3. FAISS retrieves the top relevant documents.
4. Retrieved context is passed to the LLM.
5. The LLM generates a grounded response.

### 6.7 Response Generation

Groq-hosted Llama models are used for response generation. The system uses different prompts depending on the selected mode:

- General chat
- Medical Q&A
- Research assistant

### 6.8 Sentiment Detection

The VADER sentiment analyzer detects whether the user message is:

- Positive
- Neutral
- Negative

The detected sentiment is used to adjust the tone of the response.

### 6.9 Multilingual Processing

The system uses language detection and translation.

Workflow:

```text
User input
 → Detect language
 → Translate to English
 → Generate response
 → Translate response to selected target language
```

### 6.10 Multi-modal Image Processing

For image-based queries:

1. User uploads an image.
2. The image is encoded.
3. The image and question are sent to a Groq vision-capable model.
4. The model returns a textual answer.

---

## 7. System Architecture

```text
User
 |
 v
Streamlit Interface / Next.js Frontend
 |
 v
FastAPI Backend
 |
 v
Groq Llama Models
 |
 v
FAISS Vector Database
 |
 v
MedQuAD + arXiv + User Knowledge
```

### Architecture Explanation

- The frontend collects user input.
- The FastAPI backend processes requests.
- The RAG engine retrieves relevant documents from FAISS.
- Groq Llama models generate final responses.
- Sentiment, translation, image handling, and knowledge updating are handled by backend services.

---

## 8. Tools and Technologies Used

| Component | Tool / Model |
|---|---|
| Primary UI | Streamlit |
| Advanced UI | Next.js |
| Backend | FastAPI |
| LLM Provider | Groq API |
| Text Generation | Llama model |
| Vision Understanding | Groq vision-capable Llama model |
| Voice Transcription | Groq Whisper |
| Embeddings | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| Sentiment Analysis | VADER |
| Language Detection | langdetect |
| Translation | deep-translator |
| Image Processing | Pillow |
| Web Parsing | BeautifulSoup |
| arXiv Data Collection | feedparser |

---

## 9. Note on Google PaLM / Gemini API

The internship task suggested Google PaLM/Gemini APIs for multi-modal AI capabilities. Due to billing constraints and reproducibility requirements, this project uses Groq-hosted open-source Llama models as an accessible alternative.

The core objectives remain satisfied:

- Text generation
- Image understanding
- Multi-modal interaction
- Retrieval-augmented responses
- Multilingual support
- Sentiment-aware chatbot behavior

---

## 10. Implementation Details

### 10.1 General Chat

The general chat module answers user questions using the LLM. It supports natural conversation and follow-up questions.

### 10.2 Medical Q&A

The Medical Q&A module uses MedQuAD documents as a domain-specific knowledge base. User questions are embedded and compared with medical document vectors in FAISS.

The retrieved context is passed to the LLM to generate educational medical responses.

The system also includes basic medical entity recognition for:

- Symptoms
- Diseases
- Treatments
- Body parts

### 10.3 Research Assistant

The research assistant uses arXiv paper abstracts to answer scientific and technical questions. It can explain concepts such as:

- Retrieval-augmented generation
- Transformers
- FAISS vector search
- Natural language processing
- Computer vision
- Machine learning

### 10.4 Vision AI

Users can upload images and ask questions about them. The system sends the image and question to a Groq vision model.

Example use cases:

- Describe an image
- Identify objects
- Explain visual content
- Extract visible information

### 10.5 Dynamic Knowledge Base

The knowledge base can be expanded using:

- URL input
- Text input
- File upload
- PDF upload

The system extracts text, chunks it, embeds it, and stores it in FAISS.

### 10.6 Sentiment Analytics

Sentiment analytics tracks the emotional tone of user messages. It displays counts and percentages for:

- Positive
- Neutral
- Negative

### 10.7 Multilingual Support

The chatbot supports multiple languages through detection and translation. Users can select the target language from the interface.

### 10.8 Chat Actions

The advanced interface includes:

- Copy user message
- Edit user message
- Copy waterGPT response
- Share response
- Helpful / not helpful feedback
- Export chat
- Clear chat

---

## 11. Results

### 11.1 Knowledge Base Results

```text
Total documents indexed: 16,715
Medical Q&A documents: 16,359
Research papers: 355
Custom documents: 1
```

### 11.2 Functional Results

The final system successfully performs:

- General question answering
- Medical Q&A using MedQuAD
- Research explanation using arXiv
- Image question answering
- Sentiment detection
- Multilingual response generation
- Dynamic knowledge base updates
- Source-aware answers
- Chat export and feedback collection

### 11.3 Example Outputs

#### Medical Q&A

User:

```text
What are the symptoms of diabetes?
```

waterGPT response includes symptoms such as:

- Increased thirst
- Frequent urination
- Fatigue
- Blurred vision
- Unexplained weight loss

#### Research Assistant

User:

```text
Explain retrieval augmented generation.
```

waterGPT explains RAG as a combination of information retrieval and language generation.
#### Vision AI

User uploads an image and asks:

```text
What team is this?
```

waterGPT analyzes the image and identifies the visual context.

---

## 12. Screenshots

Screenshots are included in the `screenshots` folder.

---

## 13. Evaluation Highlights

This project demonstrates:

- Full-stack AI application development
- Real dataset integration
- Retrieval-Augmented Generation
- Vector database usage
- Multi-modal AI
- Sentiment-aware conversation
- Multilingual chatbot design
- Streamlit-based required implementation
- Advanced production-style frontend
- API-based backend architecture
- Reproducible project structure

---

## 14. Limitations

- Image generation is not implemented due to free API limitations.
- Web search is not included because it may require paid external APIs.
- Medical responses are educational and not a substitute for professional diagnosis.
- Translation quality depends on external translation services.
- The arXiv subset is limited to selected computer science categories.
- Voice input may require browser permissions and may work best in supported browsers.

---

## 15. Future Scope

Future improvements include:

- Add image generation using Stable Diffusion or another accessible model
- Add user authentication
- Store chat history in a database
- Add PDF summarization mode
- Deploy backend and frontend online
- Add advanced medical NER using biomedical NLP models
- Add richer analytics and evaluation metrics
- Add source ranking and citation scores
- Add full document search interface
- Add user feedback dashboard

---

## 16. Conclusion

waterGPT demonstrates a complete AI chatbot system integrating RAG, medical Q&A, research assistance, image understanding, sentiment analysis, multilingual support, and dynamic knowledge base expansion.

The project satisfies all six internship tasks and includes both a Streamlit-based primary interface and an advanced Next.js + FastAPI implementation. The system is reproducible, documented, and structured for professional GitHub submission.

---

## 17. Disclaimer

The medical chatbot provides educational information only. It should not be used as a replacement for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical concerns.

---

## 18. Author

**Vinayak Varshith Reddy Vangeti**  
**Email:** [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com)  
**Program:** Elevance Skills Internship  
**Project:** waterGPT — Multi-modal, Multilingual RAG Chatbot