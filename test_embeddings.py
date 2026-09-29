from rag.embeddings import EmbeddingModel
import numpy as np


embedding_model = EmbeddingModel()


texts = [
    "Python lists are mutable.",
    "A Python list can be changed after creation.",
    "The weather is sunny today."
]


embeddings = embedding_model.generate_embeddings(texts)


similarity_1 = np.dot(
    embeddings[0],
    embeddings[1]
)

similarity_2 = np.dot(
    embeddings[0],
    embeddings[2]
)


print("Similarity between sentence 1 and 2:")
print(round(float(similarity_1), 4))

print("\nSimilarity between sentence 1 and 3:")
print(round(float(similarity_2), 4))