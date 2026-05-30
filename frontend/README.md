# waterGPT Frontend

The waterGPT Frontend is the advanced Next.js-based user interface for the waterGPT project. It provides a modern, responsive, and production-style experience for interacting with the AI system.

Developed as part of the **Elevance Skills Internship**, this frontend extends the primary Streamlit implementation with a richer user experience, multi-page navigation, voice input, analytics dashboards, and advanced UI components.

---

# Overview

The frontend communicates with the FastAPI backend through REST APIs and provides interfaces for:

* General conversation
* Medical question answering
* Research assistance
* Image understanding
* Dynamic knowledge base management
* Sentiment analytics
* Language configuration
* Voice interaction

The design follows a premium black-themed interface with responsive layouts optimized for desktop, tablet, and mobile devices.

---

# Key Features

## General Chat

Provides natural conversational interaction with the AI assistant.

Features:

* Multi-turn conversations
* Context-aware responses
* Source-aware answers
* Modern chat interface

---

## Medical Assistant

Dedicated interface for medical question answering.

Features:

* Medical Q&A
* MedQuAD-powered retrieval
* Healthcare information lookup
* Educational medical guidance

---

## Research Assistant

Research-focused interface powered by arXiv knowledge.

Features:

* Scientific concept explanation
* Research summaries
* Technical question answering
* Research paper retrieval

---

## Vision AI

Image understanding interface.

Features:

* Image upload
* Visual question answering
* Image analysis
* Object and scene understanding

---

## Knowledge Base Manager

Allows users to expand chatbot knowledge dynamically.

Supported inputs:

* URLs
* Plain text
* TXT files
* CSV files
* Markdown files
* PDF files

---

## Voice Input

Supports voice-enabled interaction.

Features:

* Browser audio recording
* Speech-to-text transcription
* Voice-assisted chatting
* Groq Whisper integration

---

## Analytics Dashboard

Displays sentiment-related information.

Features:

* Positive sentiment tracking
* Neutral sentiment tracking
* Negative sentiment tracking
* Analytics visualizations

---

## Language Support

Provides multilingual interaction.

Features:

* Language selection
* Translation support
* Automatic language handling

---

# Technology Stack

## Framework

* Next.js

## UI Library

* React

## Styling

* CSS
* Responsive Layouts

## Charts

* Recharts

## Markdown Rendering

* Marked

## API Communication

* Fetch API

---

# Frontend Architecture

```text
User
 |
 v
Next.js Pages
 |
 v
React Components
 |
 v
Custom Hooks
 |
 v
API Layer
 |
 v
FastAPI Backend
```

The frontend is divided into reusable components, page-level routes, hooks, and utility libraries.

---

# Folder Structure

```text
frontend
│
├── app
│   ├── analytics
│   ├── chat
│   ├── knowledge
│   ├── language
│   ├── medical
│   ├── research
│   ├── settings
│   ├── vision
│   ├── globals.css
│   ├── layout.jsx
│   └── page.jsx
│
├── components
│   ├── charts
│   ├── layout
│   └── ui
│
├── hooks
│   ├── useChat.js
│   ├── useKnowledge.js
│   └── useSettings.js
│
├── lib
│   ├── api.js
│   ├── constants.js
│   ├── helpers.js
│   └── languages.js
│
├── public
├── styles
├── package.json
├── next.config.js
├── jsconfig.json
├── .env.local
└── .env.example
```

---

# Pages

## Home

Route:

```text
/
```

Purpose:

* Landing page
* Project introduction
* Navigation hub

---

## Chat

Route:

```text
/chat
```

Purpose:

* General AI conversation
* Voice-enabled interaction

---

## Medical

Route:

```text
/medical
```

Purpose:

* Medical question answering
* Healthcare information retrieval

---

## Research

Route:

```text
/research
```

Purpose:

* Scientific research assistance
* Technical concept explanation

---

## Vision

Route:

```text
/vision
```

Purpose:

* Image upload
* Visual analysis

---

## Knowledge

Route:

```text
/knowledge
```

Purpose:

* Knowledge base expansion
* URL ingestion
* File upload

---

## Language

Route:

```text
/language
```

Purpose:

* Language selection
* Translation settings

---

## Analytics

Route:

```text
/analytics
```

Purpose:

* Sentiment analytics
* Dashboard visualization

---

## Settings

Route:

```text
/settings
```

Purpose:

* Application configuration
* User preferences

---

# Reusable Components

The frontend uses reusable React components.

## Layout Components

Located in:

```text
components/layout
```

Components:

* Navbar
* StatusBar
* AnnouncementBar
* Footer

---

## UI Components

Located in:

```text
components/ui
```

Components:

* PageTitle
* ChatInput
* ChatMessage
* SourceBlock
* SettingsRow
* KnowledgeRow
* UploadZone
* SentimentCard

---

## Chart Components

Located in:

```text
components/charts
```

Components:

* SentimentChart

---

# Environment Variables

Create a `.env.local` file inside the frontend directory.

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

This variable specifies the backend API URL.

---

# Installation

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

---

# Running the Frontend

Start the development server:

```bash
npm run dev
```

Frontend URL:

```text
http://localhost:3000
```

---

## LAN / Mobile Testing

To access the frontend from another device on the same network:

```bash
npm run dev -- --hostname 0.0.0.0
```

Open:

```text
http://YOUR_LOCAL_IP:3000
```

from a mobile device or another computer.

---

# Backend Requirement

The frontend requires the FastAPI backend to be running.

Default backend URL:

```text
http://localhost:8000
```

API Documentation:

```text
http://localhost:8000/docs
```

---

# Responsive Design

The interface is fully responsive.

Supported devices:

* Desktop
* Laptop
* Tablet
* Mobile

Responsive features include:

* Adaptive layouts
* Mobile navigation
* Flexible chat interface
* Responsive analytics dashboard

---

# User Experience Features

The frontend includes several quality-of-life features.

## Chat Features

* Send messages
* Receive AI responses
* Copy responses
* Source viewing
* Clear chat

---

## Voice Features

* Start recording
* Stop recording
* Automatic transcription
* Insert transcribed text

---

## Knowledge Features

* Upload files
* Add URLs
* Add text content
* Manage knowledge sources

---

## Analytics Features

* Sentiment monitoring
* Data visualization
* Summary statistics

---

# Future Improvements

Potential frontend enhancements include:

* User authentication
* Chat history persistence
* Theme switching
* Advanced dashboard analytics
* Real-time notifications
* Progressive Web App support
* Dark/light theme support
* Enhanced accessibility features

---

# Author

**Vinayak Varshith Reddy Vangeti**
AI/ML Intern
Elevance Skills Internship

Email: [varshithreddyy6@gmail.com](mailto:varshithreddyy6@gmail.com)

Project: waterGPT — Multi-Modal, Multilingual RAG Chatbot

---

# Note

The primary internship-compatible implementation is available in the `legacy_streamlit` folder.

This Next.js frontend is an advanced production-style extension built on top of the internship requirements.
