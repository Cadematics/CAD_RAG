import faiss
import numpy as np
import os
import pickle

VECTOR_DIM = 384
INDEX_PATH = "data/faiss/index.bin"
META_PATH = "data/faiss/meta.pkl"

class FaissVectorStore:
    def __init__(self):
        self.index = faiss.IndexFlatL2(VECTOR_DIM)
        self.id_map = {}  # faiss_id -> chunk_id

        if os.path.exists(INDEX_PATH):
            self.load()

    def add(self, vectors, chunk_ids):
        vectors = np.array(vectors).astype("float32")
        start_id = self.index.ntotal

        self.index.add(vectors)

        for i, chunk_id in enumerate(chunk_ids):
            self.id_map[start_id + i] = chunk_id

        self.save()

    def search(self, query_vector, top_k=5):
        query_vector = np.array([query_vector]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for faiss_id, dist in zip(indices[0], distances[0]):
            if faiss_id == -1:
                continue
            results.append({
                "chunk_id": self.id_map.get(faiss_id),
                "score": float(dist)
            })
        return results

    def save(self):
        os.makedirs("data/faiss", exist_ok=True)
        faiss.write_index(self.index, INDEX_PATH)
        with open(META_PATH, "wb") as f:
            pickle.dump(self.id_map, f)

    def load(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(META_PATH, "rb") as f:
            self.id_map = pickle.load(f)
