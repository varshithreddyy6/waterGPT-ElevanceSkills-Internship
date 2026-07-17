from fastapi import APIRouter, HTTPException, Query

from core.state import research_engine
from schemas.research import PaperSearchResponse, PaperSummaryResponse


router = APIRouter(
    prefix="/research",
    tags=["research"],
)


@router.get("/search", response_model=PaperSearchResponse)
def search_papers(
    query: str = Query("", description="Free-text search across title/abstract"),
    category: str = Query("", description="Filter by arXiv category, e.g. cs.AI"),
    author: str = Query("", description="Filter by author name"),
    limit: int = Query(20, ge=1, le=100),
):
    """Dedicated arXiv paper search feature (title, category, author filters)."""
    try:
        results = research_engine.search_papers(
            query=query,
            category=category,
            author=author,
            limit=limit,
        )

        return {"results": results, "count": len(results)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/paper/{paper_id}")
def get_paper(paper_id: str):
    """Fetch a single paper by arXiv id."""
    paper = research_engine.get_paper_by_id(paper_id)

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")

    return paper


@router.get("/paper/{paper_id}/summary", response_model=PaperSummaryResponse)
def summarize_paper(paper_id: str, num_sentences: int = Query(3, ge=1, le=10)):
    """
    Real NLP summarization + keyword extraction for a single paper
    (TextRank + TF-IDF), independent of the general LLM chat prompt.
    """
    paper = research_engine.get_paper_by_id(paper_id)

    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found.")

    result = research_engine.summarize_paper(paper, num_sentences=num_sentences)

    return {
        "id": paper["id"],
        "title": paper["title"],
        "summary": result["summary"],
        "keywords": result["keywords"],
    }


@router.get("/visualization/categories")
def category_distribution():
    """Category distribution data, for a bar/pie chart of the indexed corpus."""
    return {"data": research_engine.category_distribution()}


@router.get("/visualization/keywords")
def top_keywords(top_n: int = Query(20, ge=1, le=100)):
    """Corpus-wide TF-IDF keyword frequency data, for a keyword chart."""
    return {"data": research_engine.top_corpus_keywords(top_n=top_n)}


@router.get("/visualization/concept-map")
def concept_map(max_points: int = Query(150, ge=3, le=500)):
    """2D concept map (TF-IDF + SVD projection) for a scatter-plot visualization."""
    return research_engine.concept_map(max_points=max_points)