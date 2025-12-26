from django.utils import timezone

from rag.models import Paper, Chunk, IngestionJob
from rag.ingestion.loaders import load_pdf
from rag.ingestion.section_parser import detect_sections
from rag.ingestion.chunkers import fixed_chunking, section_chunking
from rag.ingestion.embedder import EmbeddingService
from rag.retrieval.vector_store import FaissVectorStore


def ingest_paper(
    paper: Paper,
    strategy: str = "section",
    chunk_size: int = 500,
    overlap: int = 50,
):
    """
    Full ingestion pipeline:
    - Load PDF
    - Parse sections
    - Chunk text
    - Store chunks
    - Embed chunks
    - Index in FAISS
    """

    # ---- Create ingestion job ----
    job = IngestionJob.objects.create(
        paper=paper,
        chunk_strategy=strategy,
        chunk_size=chunk_size,
        overlap=overlap,
        status="running",
        started_at=timezone.now(),
    )

    try:
        # ---- Load + parse PDF ----
        pages = load_pdf(paper.file_path)
        structured_text = detect_sections(pages)

        # ---- Chunking ----
        if strategy == "fixed":
            chunks_data = fixed_chunking(
                structured_text,
                chunk_size=chunk_size,
                overlap=overlap,
            )
        elif strategy == "section":
            chunks_data = section_chunking(structured_text)
        else:
            raise ValueError(f"Unknown chunking strategy: {strategy}")

        # ---- Clear old chunks (re-ingestion safe) ----
        Chunk.objects.filter(paper=paper).delete()

        # ---- Store chunks in DB ----
        chunks = []
        for idx, chunk in enumerate(chunks_data):
            c = Chunk.objects.create(
                paper=paper,
                text=chunk["text"],
                section=chunk.get("section", ""),
                page_start=chunk.get("page_start"),
                page_end=chunk.get("page_end"),
                chunk_strategy=strategy,
                chunk_index=idx,
                embedding_model="pending",
            )
            chunks.append(c)

        # ---- Embed + index chunks ----
        _embed_and_index_chunks(chunks)

        # ---- Mark success ----
        job.status = "completed"
        job.finished_at = timezone.now()
        job.save()

        paper.ingestion_status = "completed"
        paper.save()

        return job

    except Exception as e:
        # ---- Failure handling ----
        job.status = "failed"
        job.error_message = str(e)
        job.finished_at = timezone.now()
        job.save()

        paper.ingestion_status = "failed"
        paper.save()

        raise e


def _embed_and_index_chunks(chunks):
    """
    Embed chunk texts and store vectors in FAISS.
    """
    if not chunks:
        return

    embedder = EmbeddingService()
    store = FaissVectorStore()

    texts = [c.text for c in chunks]
    vectors = embedder.embed_texts(texts)

    chunk_ids = [str(c.id) for c in chunks]
    store.add(vectors, chunk_ids)

    for c in chunks:
        c.embedding_model = "all-MiniLM-L6-v2"
        c.save()
