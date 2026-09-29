from sentence_transformers import SentenceTransformer
from typing import List, Dict
import numpy as np


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")

        self.model = SentenceTransformer(MODEL_NAME)

        print("Embedding model loaded successfully.")

    def generate_embeddings(
        self,
        texts: List[str]
    ) -> np.ndarray:

        if not texts:
            return np.array([])

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

        return embeddings

    def embed_chunks(
        self,
        chunks: List[Dict]
    ) -> np.ndarray:

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        return self.generate_embeddings(texts)