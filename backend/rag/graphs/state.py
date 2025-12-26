from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class IngestionState:
    paper_id: str
    file_path: str
    chunk_strategy: str

    pages: Optional[list] = None
    structured_text: Optional[list] = None
    chunks: Optional[list] = None
    chunk_ids: Optional[list] = None
    status: str = "pending"
    error: Optional[str] = None


@dataclass
class QueryState:
    query: str
    domain: Optional[str] = None
    top_k: int = 5

    query_vector: Optional[list] = None
    retrieved: Optional[list] = None
    chunks: Optional[list] = None

    reranked: Optional[list] = None
    context: Optional[str] = None
    citations: Optional[list] = None
