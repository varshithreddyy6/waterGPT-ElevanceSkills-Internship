from core.state import rag, updater


def add_url(url: str):
    return updater.update_from_url(url)


def add_text(text: str):
    chunks = updater.chunk_text(text)

    metadata = [
        {
            "source": "manual",
            "type": "custom",
        }
        for _ in chunks
    ]

    return rag.add_documents(chunks, metadata)


def add_file_text(filename: str, text: str):
    chunks = updater.chunk_text(text)

    metadata = [
        {
            "source": filename,
            "type": "file",
        }
        for _ in chunks
    ]

    return rag.add_documents(chunks, metadata)


def stats():
    total = len(rag.documents)

    medical = sum(
        1
        for document in rag.documents
        if document.get("metadata", {}).get("source") == "medquad"
    )

    research = sum(
        1
        for document in rag.documents
        if document.get("metadata", {}).get("source") == "arxiv"
    )

    user_docs = max(total - medical - research, 0)

    return {
        "total": total,
        "medical": medical,
        "research": research,
        "user_docs": user_docs,
    }


def clear():
    rag.clear_index()

    return {
        "status": "cleared",
        "total": len(rag.documents),
    }