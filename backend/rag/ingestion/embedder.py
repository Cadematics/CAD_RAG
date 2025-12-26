from sentence_transformers import SentenceTransformer

class EmbeddingService:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def embed_texts(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

    def embed_query(self, text):
        return self.model.encode(text)
