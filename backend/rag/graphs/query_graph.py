
from langgraph.graph import StateGraph, END
from rag.graphs.state import QueryState
from rag.ingestion.embedder import EmbeddingService
from rag.retrieval.vector_store import FaissVectorStore
from rag.models import Chunk
from rag.reranking.cross_encoder import Reranker





# Node 1 — Embed Query
def embed_query_node(state: QueryState):
    embedder = EmbeddingService()
    state.query_vector = embedder.embed_query(state.query)
    return state




# Node 2 — Vector Retrieval
def retrieve_node(state: QueryState):
    store = FaissVectorStore()
    results = store.search(state.query_vector, top_k=state.top_k)
    state.retrieved = results
    return state



# Node 3 — Fetch Chunks
def fetch_chunks_node(state: QueryState):
    print("🔎 RETRIEVED IDS:", state.retrieved)

    chunk_ids = [r["chunk_id"] for r in state.retrieved]

    print("📦 CHUNK IDS:", chunk_ids)

    chunks = list(Chunk.objects.filter(id__in=chunk_ids))

    print("📄 FETCHED CHUNKS:", len(chunks))

    state.chunks = chunks
    return state

# def fetch_chunks_node(state: QueryState):
#     chunk_ids = [r["chunk_id"] for r in state.retrieved]
#     chunks = Chunk.objects.filter(id__in=chunk_ids)

#     state.chunks = list(chunks)
#     return state




# Node 4 — Assemble Context (v1)
def assemble_context_node(state: QueryState):
    context = "\n\n".join([
        f"[{i+1}] {chunk.text}"
        for i, (chunk, _) in enumerate(state.reranked)
    ])
    state.context = context
    return state



# rerank node
def rerank_node(state: QueryState):
    reranker = Reranker()
    reranked = reranker.rerank(
        state.query,
        state.chunks,
        top_k=state.top_k
    )

    state.reranked = reranked
    return state


# Citation Assembly Node
def citation_node(state: QueryState):
    citations = []

    if not state.reranked:
        state.citations = []
        return state

    # Extract raw scores
    scores = [float(score) for _, score in state.reranked]
    min_s, max_s = min(scores), max(scores)

    def normalize(score):
        # Avoid division by zero when all scores are equal
        if max_s == min_s:
            return 1.0
        return (score - min_s) / (max_s - min_s)

    for chunk, score in state.reranked:
        citations.append({
            "paper": chunk.paper.title,
            "page_start": chunk.page_start,
            "page_end": chunk.page_end,
            "chunk_id": str(chunk.id),

            # Internal / debug
            "rerank_score": float(score),

            # UI-friendly (0–1)
            "relevance": round(normalize(float(score)), 3),
        })

    state.citations = citations
    return state






# Graph

def build_query_graph():
    graph = StateGraph(QueryState)

    graph.add_node("embed_query", embed_query_node)
    graph.add_node("retrieve", retrieve_node)
    graph.add_node("fetch_chunks", fetch_chunks_node)
    graph.add_node("rerank", rerank_node)
    graph.add_node("assemble_context", assemble_context_node)
    graph.add_node("citations", citation_node)

    graph.set_entry_point("embed_query")

    graph.add_edge("embed_query", "retrieve")
    graph.add_edge("retrieve", "fetch_chunks")
    graph.add_edge("fetch_chunks", "rerank")
    graph.add_edge("rerank", "assemble_context")
    graph.add_edge("assemble_context", "citations")
    graph.add_edge("citations", END)

    return graph.compile()



