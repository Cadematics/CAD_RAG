from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingService:
    def __init__(self, model_name="sentence-transformers/all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        vectors = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return vectors

    def embed_query(self, query):
        vectors = self.model.encode(
            [query],  # IMPORTANT: list, not string
            convert_to_numpy=True,
            normalize_embeddings=True,
        )
        return vectors[0]
