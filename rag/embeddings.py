import os
import requests
import numpy as np
from dotenv import load_dotenv


load_dotenv()


class EmbeddingModel:

    def __init__(self):

        self.api_key = os.getenv("HF_TOKEN")

        if not self.api_key:
            raise ValueError(
                "HF_TOKEN is not set in the .env file."
            )

        self.model_name = (
            "sentence-transformers/all-MiniLM-L6-v2"
        )

        # IMPORTANT:
        # Explicitly use the feature-extraction pipeline.
        self.api_url = (
            "https://router.huggingface.co/"
            "hf-inference/models/"
            f"{self.model_name}"
            "/pipeline/feature-extraction"
        )

    def generate_embeddings(self, texts):

        if not texts:
            return np.array([])

        response = requests.post(
            self.api_url,
            headers={
                "Authorization":
                    f"Bearer {self.api_key}",
                "Content-Type":
                    "application/json"
            },
            json={
                "inputs": texts,
                "normalize": True
            },
            timeout=120
        )

        if response.status_code != 200:

            raise RuntimeError(
                "Hugging Face embedding request failed: "
                f"{response.status_code} "
                f"{response.text}"
            )

        embeddings = response.json()

        embeddings = np.asarray(
            embeddings,
            dtype="float32"
        )

        # Hugging Face feature extraction can return
        # token-level embeddings with shape:
        #
        # (number_of_texts, tokens, 384)
        #
        # We mean-pool the token embeddings to obtain
        # one 384-dimensional vector per text.
        if embeddings.ndim == 3:

            embeddings = embeddings.mean(
                axis=1
            )

        # If a single embedding is returned as
        # (384,), convert it to (1, 384).
        if embeddings.ndim == 1:

            embeddings = embeddings.reshape(
                1,
                -1
            )

        # Normalize embeddings so that FAISS
        # Inner Product behaves like cosine similarity.
        norms = np.linalg.norm(
            embeddings,
            axis=1,
            keepdims=True
        )

        norms[norms == 0] = 1

        embeddings = (
            embeddings / norms
        )

        return embeddings.astype(
            "float32"
        )

    def embed_chunks(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        return self.generate_embeddings(
            texts
        )