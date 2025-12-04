from dotenv import load_dotenv

load_dotenv()


from langchain_google_vertexai import VertexAIEmbeddings
import numpy as np


target_texts = ["漫画", "アニメ"]
model = VertexAIEmbeddings(
    model="text-multilingual-embedding-002",
    # model="gemini-embedding-001",
    # dimensions=768,
)
results = model.embed(
    target_texts,
    embeddings_task_type="SEMANTIC_SIMILARITY",
)

embedding1 = np.array(results[0])
embedding2 = np.array(results[1])

print(f"{target_texts[0]}: {embedding1[:5]}...({len(embedding1)}dimensions)")
print(f"{target_texts[1]}: {embedding2[:5]}...({len(embedding2)}dimensions)")

normed_embedding1 = embedding1 / np.linalg.norm(embedding1)
normed_embedding2 = embedding2 / np.linalg.norm(embedding2)
print("cosine similarity: ", np.dot(normed_embedding1, normed_embedding2))
