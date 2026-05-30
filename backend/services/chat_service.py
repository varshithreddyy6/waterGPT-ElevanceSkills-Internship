from config import MODEL_NAME
from core.groq_client import client
from core.prompts import SYSTEM_PROMPTS
from core.state import rag, sentiment_analyzer, translator

from services.medical_ner_service import extract_medical_entities


def max_tokens_for_length(length: str) -> int:
    return {
        "short": 550,
        "medium": 1024,
        "long": 1800,
    }.get(length, 1024)


def is_simple_message(text: str) -> bool:
    text = text.strip().lower()

    simple_messages = [
        "hi",
        "hello",
        "hey",
        "hii",
        "hai",
        "yo",
        "good morning",
        "good afternoon",
        "good evening",
        "how are you",
        "who are you",
        "what is your name",
        "thanks",
        "thank you",
        "ok",
        "okay",
    ]

    return text in simple_messages


def normalize_history(history):
    normalized = []

    for msg in history[-8:]:
        role = getattr(msg, "role", None) or msg.get("role", "")
        content = getattr(msg, "content", None) or msg.get("content", "")

        if not content:
            continue

        if role == "bot":
            role = "assistant"

        if role not in ["user", "assistant"]:
            continue

        normalized.append(
            {
                "role": role,
                "content": content,
            }
        )

    return normalized


def generate_response(
    query,
    context="",
    sentiment_info=None,
    mode="chat",
    response_length="medium",
    history=None,
):
    system_prompt = SYSTEM_PROMPTS.get(
        mode,
        SYSTEM_PROMPTS["chat"],
    )

    if sentiment_info:
        system_prompt += " " + sentiment_analyzer.get_response_tone(
            sentiment_info.get("sentiment", "neutral")
        )

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    if context:
        messages.append(
            {
                "role": "system",
                "content": f"Use this retrieved context when relevant:\n\n{context}",
            }
        )

    if history:
        messages.extend(normalize_history(history))

    messages.append(
        {
            "role": "user",
            "content": query,
        }
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=0.7,
        max_tokens=max_tokens_for_length(response_length),
    )

    return response.choices[0].message.content


def handle_chat(
    message: str,
    mode="chat",
    target_language="en",
    response_length="medium",
    history=None,
):
    english_query, detected_language = translator.translate_to_english(message)

    sentiment_info = sentiment_analyzer.analyze(english_query)

    sources = []
    context = ""

    if not is_simple_message(english_query):
        sources = rag.search(
            english_query,
            top_k=3,
        )

        if sources:
            context = "\n\n".join(
                [
                    source.get("text", "")
                    for source in sources
                ]
            )

    answer = generate_response(
        query=english_query,
        context=context,
        sentiment_info=sentiment_info,
        mode=mode,
        response_length=response_length,
        history=history or [],
    )

    if target_language != "en":
        answer = translator.translate_from_english(
            answer,
            target_language,
        )

    medical_entities = {}

    if mode == "medical":
        medical_entities = extract_medical_entities(english_query)

    return {
        "answer": answer,
        "sentiment": sentiment_info,
        "detected_language": detected_language,
        "sources": sources,
        "medical_entities": medical_entities,
    }