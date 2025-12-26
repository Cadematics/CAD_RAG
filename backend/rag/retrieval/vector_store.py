import faiss
import numpy as np
import pickle
from pathlib import Path
from django.conf import settings

VECTOR_DIM = 384

# Absolute, stable paths (no cwd surprises)
FAISS_DIR = Path(settings.BASE_DIR) / "data" / "faiss"
INDEX_PATH = FAISS_DIR / "index.bin"
META_PATH = FAISS_DIR / "meta.pkl"


class FaissVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(VECTOR_DIM)
        self.id_map = {}  # faiss_id -> chunk_id (uuid str)

        if INDEX_PATH.exists() and META_PATH.exists():
            self.load()

    def add(self, vectors, chunk_ids):
        vectors = np.asarray(vectors, dtype="float32")

        if vectors.ndim != 2 or vectors.shape[1] != VECTOR_DIM:
            raise ValueError(f"Expected vectors shape (N, {VECTOR_DIM}), got {vectors.shape}")

        start_id = self.index.ntotal
        self.index.add(vectors)

        for i, chunk_id in enumerate(chunk_ids):
            self.id_map[start_id + i] = chunk_id

        self.save()

    def search(self, query_vector, top_k=5):
        if self.index.ntotal == 0:
            return []

        q = np.asarray(query_vector, dtype="float32")
        if q.ndim != 1 or q.shape[0] != VECTOR_DIM:
            raise ValueError(f"Expected query_vector shape ({VECTOR_DIM},), got {q.shape}")

        distances, indices = self.index.search(q.reshape(1, -1), min(top_k, self.index.ntotal))

        results = []
        for faiss_id, dist in zip(indices[0], distances[0]):
            if faiss_id == -1:
                continue
            results.append({
                "chunk_id": self.id_map.get(int(faiss_id)),
                "score": float(dist),
            })
        return results

    def save(self):
        FAISS_DIR.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(INDEX_PATH))
        with open(META_PATH, "wb") as f:
            pickle.dump(self.id_map, f)

    def load(self):
        self.index = faiss.read_index(str(INDEX_PATH))
        with open(META_PATH, "rb") as f:
            self.id_map = pickle.load(f)
