import io
import requests
from datetime import datetime

import streamlit as st


# ============================================================
# CONFIG
# ============================================================

API_BASE = "http://localhost:8000"

st.set_page_config(
    page_title="waterGPT | Streamlit Internship Demo",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# CSS
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,500;0,600;1,400;1,500;1,600&family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
    background: #000000 !important;
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #222222;
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-family: 'Playfair Display', serif !important;
}

.main-title {
    font-family: 'Playfair Display', serif;
    font-size: 72px;
    font-weight: 500;
    font-style: italic;
    line-height: 0.95;
    margin-bottom: 10px;
}

.subtitle {
    color: #aaaaaa;
    font-size: 14px;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 30px;
}

.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 44px;
    margin-top: 20px;
    margin-bottom: 10px;
}

.task-box {
    border: 1px solid #333333;
    padding: 18px;
    margin-bottom: 14px;
    background: #050505;
}

.task-label {
    font-size: 12px;
    letter-spacing: 3px;
    color: #888888;
    text-transform: uppercase;
}

.task-value {
    font-size: 24px;
    font-weight: 600;
    color: #ffffff;
}

.stTextInput input, .stTextArea textarea {
    background: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 0 !important;
}

.stSelectbox div {
    background: #000000 !important;
    color: #ffffff !important;
}

.stButton button {
    background: #000000 !important;
    color: #ffffff !important;
    border: 1px solid #ffffff !important;
    border-radius: 0 !important;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-size: 12px;
    padding: 10px 24px;
}

.stButton button:hover {
    background: #ffffff !important;
    color: #000000 !important;
}

.stFileUploader {
    background: #000000 !important;
}

.stAlert {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #333333 !important;
}

.chat-user {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    margin-bottom: 12px;
}

.chat-bot-title {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    font-style: italic;
    margin-top: 20px;
}

.source-box {
    border-top: 1px solid #333333;
    padding-top: 14px;
    margin-top: 20px;
    color: #aaaaaa;
    font-size: 12px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.footer {
    text-align: center;
    margin-top: 70px;
    padding-top: 30px;
    border-top: 1px solid #222222;
    color: #555555;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}

.metric-card {
    border: 1px solid #222222;
    background: #050505;
    padding: 18px;
    text-align: center;
}

.metric-number {
    font-family: 'Playfair Display', serif;
    font-size: 48px;
}

.metric-label {
    color: #999999;
    font-size: 11px;
    letter-spacing: 3px;
    text-transform: uppercase;
}

</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = {
        "chat": [],
        "medical": [],
        "research": [],
    }

if "sentiment_history" not in st.session_state:
    st.session_state.sentiment_history = []

if "target_language" not in st.session_state:
    st.session_state.target_language = "en"

if "response_length" not in st.session_state:
    st.session_state.response_length = "medium"


# ============================================================
# API HELPERS
# ============================================================

def api_get(path):
    response = requests.get(f"{API_BASE}{path}", timeout=60)
    response.raise_for_status()
    return response.json()


def api_post_json(path, payload):
    response = requests.post(f"{API_BASE}{path}", json=payload, timeout=180)
    response.raise_for_status()
    return response.json()


def api_post_file(path, files, data=None):
    response = requests.post(f"{API_BASE}{path}", files=files, data=data, timeout=180)
    response.raise_for_status()
    return response.json()


def get_stats():
    try:
        return api_get("/knowledge/stats")
    except Exception:
        return {
            "total": 0,
            "medical": 0,
            "research": 0,
            "user_docs": 0,
        }


def call_chat(message, mode):
    payload = {
        "message": message,
        "mode": mode,
        "target_language": st.session_state.target_language,
        "response_length": st.session_state.response_length,
    }

    data = api_post_json("/chat", payload)

    sentiment = data.get("sentiment", {})
    st.session_state.sentiment_history.append(sentiment.get("sentiment", "neutral"))

    return data


def now_time():
    return datetime.now().strftime("%H:%M")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.markdown("## waterGPT Controls")
    st.caption("Developed by Vinayak Varshith Reddy Vangeti")
    st.caption("varshithreddyy6@gmail.com")

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "General Chat",
            "Medical Q&A",
            "Research Assistant",
            "Vision AI",
            "Knowledge Base",
            "Sentiment Analytics",
            "Language Settings",
        ],
    )

    st.markdown("---")

    st.session_state.target_language = st.selectbox(
        "Target Language",
        ["en", "hi", "te", "ta", "es", "fr", "de", "ar", "zh-CN", "ja"],
        format_func=lambda x: {
            "en": "English",
            "hi": "Hindi",
            "te": "Telugu",
            "ta": "Tamil",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ar": "Arabic",
            "zh-CN": "Chinese",
            "ja": "Japanese",
        }.get(x, x),
    )

    st.session_state.response_length = st.selectbox(
        "Response Length",
        ["short", "medium", "long"],
        index=["short", "medium", "long"].index(st.session_state.response_length),
    )

    st.markdown("---")

    if st.button("Refresh Knowledge Stats"):
        st.rerun()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="main-title">waterGPT</div>
<div class="subtitle">Multi-modal · Multilingual · Intelligent · RAG Chatbot</div>
""",
    unsafe_allow_html=True,
)


# ============================================================
# OVERVIEW PAGE
# ============================================================

if page == "Overview":
    stats = get_stats()

    st.markdown('<div class="section-title">Internship Project Overview</div>', unsafe_allow_html=True)

    st.write(
        """
        waterGPT is a full-stack AI chatbot project built for the Elevance Skills Internship.
        This Streamlit interface is the primary internship-compatible demo and connects to the same FastAPI backend used by the advanced Next.js interface.
        """
    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{stats.get("total", 0):,}</div>
                <div class="metric-label">Total Documents</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{stats.get("medical", 0):,}</div>
                <div class="metric-label">Medical Q&As</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{stats.get("research", 0):,}</div>
                <div class="metric-label">Research Papers</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">{stats.get("user_docs", 0):,}</div>
                <div class="metric-label">User Docs</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Internship Tasks Covered")

    tasks = [
        ("01", "Dynamic Knowledge Base", "URL, text, and file ingestion with FAISS updates"),
        ("02", "Multi-modal Chatbot", "Image understanding using Groq vision model"),
        ("03", "Medical Q&A", "MedQuAD-based retrieval augmented medical chatbot"),
        ("04", "Research Assistant", "arXiv paper retrieval and scientific explanation"),
        ("05", "Sentiment Analysis", "VADER sentiment detection and adaptive response tone"),
        ("06", "Multilingual Support", "Language detection and translation support"),
    ]

    for num, title, desc in tasks:
        st.markdown(
            f"""
            <div class="task-box">
                <div class="task-label">{num}</div>
                <div class="task-value">{title}</div>
                <p>{desc}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ============================================================
# CHAT PAGES
# ============================================================

def render_chat_page(mode, title, placeholder):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)

    messages = st.session_state.messages[mode]

    for msg in messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-user">You: {msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="chat-bot-title">waterGPT</div>', unsafe_allow_html=True)
            st.markdown(msg["content"])

            if msg.get("sources"):
                st.markdown(
                    f'<div class="source-box">Sources ({len(msg["sources"])}) · Knowledge Base</div>',
                    unsafe_allow_html=True,
                )

            if msg.get("medical_entities"):
                st.markdown("**Medical Entities:**")
                st.json(msg["medical_entities"])

    with st.form(key=f"{mode}_form", clear_on_submit=True):
        user_input = st.text_area("Your Question", placeholder=placeholder, height=130)
        submitted = st.form_submit_button("Ask waterGPT")

    if submitted and user_input.strip():
        messages.append(
            {
                "role": "user",
                "content": user_input,
                "time": now_time(),
            }
        )

        with st.spinner("waterGPT is thinking..."):
            try:
                data = call_chat(user_input, mode)

                messages.append(
                    {
                        "role": "bot",
                        "content": data.get("answer", ""),
                        "sources": data.get("sources", []),
                        "medical_entities": data.get("medical_entities", {}),
                        "sentiment": data.get("sentiment", {}),
                    }
                )

                st.rerun()

            except Exception as e:
                st.error(f"Error: {e}")


if page == "General Chat":
    render_chat_page(
        mode="chat",
        title="General Chat",
        placeholder="Ask anything...",
    )


if page == "Medical Q&A":
    render_chat_page(
        mode="medical",
        title="Medical Q&A using MedQuAD",
        placeholder="Ask a medical question...",
    )


if page == "Research Assistant":
    render_chat_page(
        mode="research",
        title="arXiv Research Assistant",
        placeholder="Ask about research papers, AI, ML, NLP, or scientific concepts...",
    )


# ============================================================
# VISION PAGE
# ============================================================

if page == "Vision AI":
    st.markdown('<div class="section-title">Vision AI</div>', unsafe_allow_html=True)

    st.write("Upload an image and ask a question about it.")

    uploaded_image = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg", "webp"],
    )

    question = st.text_input(
        "Question about image",
        placeholder="Describe this image...",
    )

    if uploaded_image:
        st.image(uploaded_image, width=500)

    if st.button("Analyze Image"):
        if not uploaded_image:
            st.warning("Please upload an image first.")
        elif not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Analyzing image..."):
                try:
                    files = {
                        "image": (
                            uploaded_image.name,
                            uploaded_image.getvalue(),
                            uploaded_image.type,
                        )
                    }

                    data = {
                        "question": question,
                        "target_language": st.session_state.target_language,
                    }

                    result = api_post_file("/vision", files=files, data=data)

                    st.markdown('<div class="chat-bot-title">waterGPT Vision</div>', unsafe_allow_html=True)
                    st.markdown(result.get("answer", ""))

                except Exception as e:
                    st.error(f"Vision error: {e}")


# ============================================================
# KNOWLEDGE BASE PAGE
# ============================================================

if page == "Knowledge Base":
    st.markdown('<div class="section-title">Dynamic Knowledge Base</div>', unsafe_allow_html=True)

    stats = get_stats()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Documents", f"{stats.get('total', 0):,}")
    c2.metric("Medical Q&As", f"{stats.get('medical', 0):,}")
    c3.metric("Research Papers", f"{stats.get('research', 0):,}")
    c4.metric("User Docs", f"{stats.get('user_docs', 0):,}")

    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["Add URL", "Add Text", "Add File"])

    with tab1:
        url = st.text_input("URL", placeholder="Paste URL...")
        if st.button("Add URL to Knowledge Base"):
            if url.strip():
                with st.spinner("Fetching and indexing URL..."):
                    try:
                        result = api_post_json("/knowledge/url", {"url": url})
                        st.success(f"Added {result.get('added_chunks', 0)} chunks.")
                    except Exception as e:
                        st.error(e)

    with tab2:
        text = st.text_area("Text Content", height=220)
        if st.button("Add Text to Knowledge Base"):
            if text.strip():
                with st.spinner("Indexing text..."):
                    try:
                        result = api_post_json("/knowledge/text", {"text": text})
                        st.success(f"Added {result.get('added_chunks', 0)} chunks.")
                    except Exception as e:
                        st.error(e)

    with tab3:
        file = st.file_uploader("Upload txt/md/csv", type=["txt", "md", "csv"])
        if st.button("Process File"):
            if file:
                with st.spinner("Indexing file..."):
                    try:
                        files = {
                            "file": (
                                file.name,
                                file.getvalue(),
                                "text/plain",
                            )
                        }

                        result = api_post_file("/knowledge/file", files=files)
                        st.success(f"Added {result.get('added_chunks', 0)} chunks.")
                    except Exception as e:
                        st.error(e)


# ============================================================
# SENTIMENT ANALYTICS PAGE
# ============================================================

if page == "Sentiment Analytics":
    st.markdown('<div class="section-title">Sentiment Analytics</div>', unsafe_allow_html=True)

    history = st.session_state.sentiment_history

    positive = history.count("positive")
    neutral = history.count("neutral")
    negative = history.count("negative")
    total = positive + neutral + negative or 1

    c1, c2, c3 = st.columns(3)

    c1.metric("Positive", f"{int((positive / total) * 100)}%")
    c2.metric("Neutral", f"{int((neutral / total) * 100)}%")
    c3.metric("Negative", f"{int((negative / total) * 100)}%")

    st.markdown("### Raw Counts")
    st.json(
        {
            "positive": positive,
            "neutral": neutral,
            "negative": negative,
            "total": positive + neutral + negative,
        }
    )

    if st.button("Clear Sentiment History"):
        st.session_state.sentiment_history = []
        st.rerun()


# ============================================================
# LANGUAGE SETTINGS PAGE
# ============================================================

if page == "Language Settings":
    st.markdown('<div class="section-title">Language Settings</div>', unsafe_allow_html=True)

    st.write("Select a target language from the sidebar.")

    st.info(
        f"Current selected language: {st.session_state.target_language.upper()}"
    )

    st.markdown(
        """
        Supported languages include English, Hindi, Telugu, Tamil, Spanish, French,
        German, Arabic, Chinese, Japanese and more.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
waterGPT · Powered by Groq · Llama 3.3 70B<br>
Developed by Vinayak Varshith Reddy Vangeti · varshithreddyy6@gmail.com
</div>
""",
    unsafe_allow_html=True,
)