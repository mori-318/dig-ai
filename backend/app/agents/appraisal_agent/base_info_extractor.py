from unittest import result

from google import genai
from google.genai import types
import json

PROMPT_TEMPLATE = """
与えられた画像から、以下の情報を抽出して、出力形式に従ってJSON形式で出力してください。
出力はJSONオブジェクトのみ。コードフェンスや説明文などの余計な文字は一切付けないでください。


## 抽出する情報
- ブランド: Chumpion, Nikeなど
- カテゴリ: Tシャツ、スニーカーなど

## 出力形式
{
  "brand": "ブランド名",
  "category": "カテゴリ名",
  "retake_required": true or false,
  "retake_instructions": "ブランド名が写るようになど、**日本語**の再撮影の指示"
}

### 出力例（成功時）
{
  "brand": "Nike",
  "category": "スニーカー",
  "retake_required": false,
  "retake_instructions": ""
}

### 出力例（再撮影が必要な場合）
{
  "brand": "",
  "category": "スウェットシャツ",
  "retake_required": true,
  "retake_instructions": "スウェットシャツであることはわかりました。ブランド名が写るように再撮影してください"
}
"""

class BaseInfoExtractor:
    def __init__(self, gemini_client: genai.Client, model="gemini-2.5-flash-lite"):
        self.gemini_client = gemini_client
        self.model = model

    def run(self, image_bytes: bytes) -> dict:
        response = self.gemini_client.models.generate_content(
            model=self.model,
            contents=[
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type="image/png",
                ),
                PROMPT_TEMPLATE
            ],
            config={
                "response_mime_type": "application/json",
            }
        )
        return json.loads(response.text)
