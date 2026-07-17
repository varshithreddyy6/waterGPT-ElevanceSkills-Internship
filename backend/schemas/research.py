from typing import List

from pydantic import BaseModel


class PaperResult(BaseModel):
    id: str
    title: str
    authors: str
    categories: str
    primary_category: str
    abstract: str
    published: str
    link: str


class PaperSearchResponse(BaseModel):
    results: List[PaperResult]
    count: int


class PaperSummaryResponse(BaseModel):
    id: str
    title: str
    summary: str
    keywords: List[str]