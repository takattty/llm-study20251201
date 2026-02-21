import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

client = genai.Client(api_key = os.getenv("GENAI_API_KEY"))

# ファイルから画像を読み込む
with open("data/sample_image.png", "rb") as f:
    image_bytes = f.read()

# 演習: ここで画像を含むマルチモーダルな入力を送ってみよう
# ヒント: types.Part.from_bytes を使って画像をパートとして追加
# contentsにはリストで画像パートとテキストを両方渡すことができます
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    # 演習: ここに画像とテキストのプロンプトを含むリストを渡そう
    # ヒント: contents=[types.Part.from_bytes(data=..., mime_type="image/png"), "指示プロンプト"]
    contents=[types.Part.from_bytes(data=image_bytes, mime_type="image/png"), "この画像に写っているものを説明してください。"],
)

print(response.text)

