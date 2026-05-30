from utils.rag_engine import RAGEngine


def test_rag_initializes():
    rag = RAGEngine()

    assert rag.index is not None
    assert isinstance(rag.documents, list)