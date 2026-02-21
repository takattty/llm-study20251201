import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
import numpy as np
from google.genai import types

client = genai.Client(api_key = os.getenv("GENAI_API_KEY"))


target_texts = ["今日はJavaを使わずにLLMの勉強資料を進めました。", "昨年の手術は上顎の骨を削るもので、かなり麻酔が効いており進行には余裕を持って行えました。"]
# 演習: ここでEmbedding APIを使って2つのテキストをベクトル化しよう
result = client.models.embed_content(
    # 演習: ここでモデル名を指定しよう（text-multilingual-embedding-002 など）
    model="gemini-embedding-001",
    # 演習: ここでベクトル化したいテキストのリストを渡そう
    contents=target_texts,
    config=types.EmbedContentConfig(
        # 演習: ここでタスクタイプを指定しよう
        # task_type は "SEMANTIC_SIMILARITY" を指定
        task_type="SEMANTIC_SIMILARITY",
    ),
)

embedding1 = np.array(result.embeddings[0].values)
embedding2 = np.array(result.embeddings[1].values)

print(f"{target_texts[0]}: {embedding1[:5]}...({len(embedding1)}dimensions)")
print(f"{target_texts[1]}: {embedding2[:5]}...({len(embedding2)}dimensions)")

# 演習: ここでコサイン類似度を計算しよう
similarity = np.dot(embedding1, embedding2) / (np.linalg.norm(embedding1) * np.linalg.norm(embedding2))
print("cosine similarity: ", similarity)
