import faiss
import numpy as np
from typing import List, Dict


class VectorRetriever:

    def __init__(self):
        self.index = None
        self.chunks = []

    def build_index(
        self,
        embeddings: np.ndarray,
        chunks: List[Dict]
    ):
        """
        Build a FAISS vector index from document embeddings.
        """

        if embeddings.size == 0:
            raise ValueError(
                "No embeddings available to build the index."
            )

        # FAISS expects float32
        embeddings = embeddings.astype("float32")

        # Number of dimensions in each embedding
        dimension = embeddings.shape[1]

        # Inner Product works as cosine similarity
        # because embeddings were normalized
        self.index = faiss.IndexFlatIP(dimension)

        # Add document embeddings
        self.index.add(embeddings)

        # Keep original chunks so we can retrieve
        # the actual PDF text later
        self.chunks = chunks

    def search(
        self,
        query_embedding: np.ndarray,
        top_k: int = 5
    ) -> List[Dict]:
        """
        Search the FAISS index and return the most
        relevant document chunks.
        """

        if self.index is None:
            raise ValueError(
                "No document has been uploaded yet."
            )

        query_embedding = query_embedding.astype(
            "float32"
        )

        # FAISS expects shape:
        # (number_of_queries, embedding_dimensions)

        if query_embedding.ndim == 1:
            query_embedding = query_embedding.reshape(
                1, -1
            )

        # Do not request more results than available chunks
        actual_top_k = min(
            top_k,
            len(self.chunks)
        )

        scores, indices = self.index.search(
            query_embedding,
            actual_top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            chunk = self.chunks[index].copy()

            chunk["similarity_score"] = float(
                score
            )

            results.append(chunk)

        return results