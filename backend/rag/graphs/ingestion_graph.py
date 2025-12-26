from langgraph.graph import StateGraph, END
from rag.graphs.state import IngestionState
from rag.models import Paper, Chunk
from rag.ingestion.loaders import load_pdf
from rag.ingestion.section_parser import detect_sections
from rag.ingestion.chunkers import fixed_chunking, section_chunking
from rag.ingestion.pipeline import _embed_and_index_chunks




# node 1
def load_pdf_node(state: IngestionState):
    pages = load_pdf(state.file_path)
    state.pages = pages
    return state



#Node 2 — Detect Sections
def detect_sections_node(state: IngestionState):
    structured = detect_sections(state.pages)
    state.structured_text = structured
    return state



# Node 3 — Chunk Text
def chunk_node(state: IngestionState):
    if state.chunk_strategy == "fixed":
        chunks = fixed_chunking(state.structured_text)
    else:
        chunks = section_chunking(state.structured_text)

    state.chunks = chunks
    return state




# Node 4 — Persist + Embed
def persist_and_embed_node(state: IngestionState):
    paper = Paper.objects.get(id=state.paper_id)

    Chunk.objects.filter(paper=paper).delete()

    chunk_models = []
    for idx, chunk in enumerate(state.chunks):
        c = Chunk.objects.create(
            paper=paper,
            text=chunk["text"],
            section=chunk.get("section", ""),
            page_start=chunk.get("page_start"),
            page_end=chunk.get("page_end"),
            chunk_strategy=state.chunk_strategy,
            chunk_index=idx,
            embedding_model="pending",
        )
        chunk_models.append(c)

    _embed_and_index_chunks(chunk_models)

    state.chunk_ids = [str(c.id) for c in chunk_models]
    state.status = "completed"
    return state






# Graph
def build_ingestion_graph():
    graph = StateGraph(IngestionState)

    graph.add_node("load_pdf", load_pdf_node)
    graph.add_node("detect_sections", detect_sections_node)
    graph.add_node("chunk", chunk_node)
    graph.add_node("persist_and_embed", persist_and_embed_node)

    graph.set_entry_point("load_pdf")

    graph.add_edge("load_pdf", "detect_sections")
    graph.add_edge("detect_sections", "chunk")
    graph.add_edge("chunk", "persist_and_embed")
    graph.add_edge("persist_and_embed", END)

    return graph.compile()
