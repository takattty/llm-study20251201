from dotenv import load_dotenv

load_dotenv()


from langchain_google_vertexai import VertexAIEmbeddings
import numpy as np


target_texts = ["漫画", "アニメ"]
# 演習: ここでEmbeddingモデルを作成しよう
model = VertexAIEmbeddings(
    # 演習: ここでモデル名を指定しよう（text-multilingual-embedding-002 など）
    model="",
)
# 演習: ここでテキストをベクトル化しよう
results = model.embed(
    target_texts,
    # 演習: ここでタスクタイプを指定しよう
    # task_type は "SEMANTIC_SIMILARITY" を指定
    embeddings_task_type="",
)


embedding1 = np.array(results[0])
embedding2 = np.array(results[1])

print(f"{target_texts[0]}: {embedding1[:5]}...({len(embedding1)}dimensions)")
print(f"{target_texts[1]}: {embedding2[:5]}...({len(embedding2)}dimensions)")

# 演習: ここでコサイン類似度を計算しよう
similarity = None
print("cosine similarity: ", similarity)
