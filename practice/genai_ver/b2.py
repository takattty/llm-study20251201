import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
from pydantic import BaseModel, Field
from google.genai.types import GenerateContentConfig

client = genai.Client(api_key = os.getenv("GENAI_API_KEY"))


# 演習: コメントから商品名、ポジティブな点、ネガティブな点、スコアを抽出するクラスを定義しよう
class CommentAnalysis(BaseModel):
    # 演習: ここに4つのフィールドを定義しよう(str, intなど適切な型を使う)
    product_name: str = Field(description="商品名")
    positive_points: str = Field(description="ポジティブな点")
    negative_points: str = Field(description="ネガティブな点")
    score: int = Field(description="5段階のスコア: ポジティブな点とネガティブな点を総合して計算")


input_text = "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。"
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    # 演習: ここにコメントを分析するプロンプトを書こう
    contents=f"""以下のコメントの分析をしてくださ: {input_text}""",
    config=GenerateContentConfig(
        response_mime_type="application/json",
        # 演習: ここで構造化出力のスキーマを指定しよう
        response_schema=CommentAnalysis,
        temperature=0.1,
    ),
)
comment_result = CommentAnalysis.model_validate_json(response.text)
print(comment_result)
