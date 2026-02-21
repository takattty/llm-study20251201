from dotenv import load_dotenv

load_dotenv()
import os
from google import genai
from pydantic import BaseModel, Field
from typing import Literal
from google.genai.types import GenerateContentConfig

client = genai.Client(api_key = os.getenv("GENAI_API_KEY"))

# 演習: コメントの感情（ポジティブ/ネガティブ/ニュートラル）を分類するためのクラスを定義しよう
# ヒント: Literal["aaa", "bbb", "ccc"] のようにLiteral[]を使うと選択肢を制限できます
class CommentAnalysis(BaseModel):
    # 演習: 「ここに...書いてね」の部分を埋めて完成させよう
    # LLMが返すJSONのフィールドの説明＝どう答えるか＝LLMへの判断基準
    # ここがこの問題の大事な部分で、LLMが勝手に判断しないように、形式を制御する！！！
    sentiment: Literal["positive", "negative", "neutral"] = Field(
        description="""
                    コメントの感情判定:
                    - positive: 製品に満足、褒めている、推奨している
                    - negative: 不満、批判、改善要望がある
                    - neutral: 中立的、事実述べ、どちらとも言えない
                    """
    )

    # int でも可能
    # sentiment: int = Field(description="-1: ネガティブ, 0: ニュートラル, 1: ポジティブ", ge=-1, le=1)


input_text = "スマート加湿器を購入。静音性は期待通り。給水が面倒なのがマイナス。5点満点中3点といったところ。"
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    # 演習: ここにコメントの感情を判定するプロンプトを書こう
    # ユーザーがLLMにやってもらうタスク指示＝何をするかの記述
    contents=f"""以下のコメントの感情をpositive/negative/neutralで判定してください: {input_text}""",
    config=GenerateContentConfig(
        # 演習: response_schema に上で定義した CommentAnalysis クラスを指定して構造化出力を完成させよう
        response_mime_type="application/json",
        response_schema=CommentAnalysis,
        temperature=0.1,
    ),
)
comment_result = CommentAnalysis.model_validate_json(response.text)
print(comment_result)
