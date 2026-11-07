
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):
        self.model_name = (
            "sentence-transformers/"
            "paraphrase-multilingual-MiniLM-L12-v2"
        )

        # Load the embedding model once
        self.model = SentenceTransformer(self.model_name)

    def generate_embeddings(self, texts: list[str]):
        """
        Convert a list of text strings into numerical vectors.
        """

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=True
        )

        return embeddings
