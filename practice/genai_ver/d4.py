import os
from dotenv import load_dotenv

load_dotenv()

from google import genai
from google.genai import types

client = genai.Client(api_key = os.getenv("GENAI_API_KEY"))


def get_current_temperature(location: str) -> dict[str, str]:
    """指定した場所の現在の気温を返す"""
    # ダミー実装
    return types.Tool(google_search=types.GoogleSearch())


def get_current_humidity(location: str) -> dict[str, str]:
    """指定した場所の現在の湿度を返す"""
    # ダミー実装
    return {"location": location, "湿度": "60%"}


response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="今日の東京の気温と湿度を調べてください",
    config=types.GenerateContentConfig(
        tools=[get_current_temperature, get_current_humidity]
    ),
)

print(response.text)

