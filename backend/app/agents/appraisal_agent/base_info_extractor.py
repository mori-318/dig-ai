"""画像からブランド・カテゴリと再撮影要否を抽出する処理。"""

import json

from google import genai
from google.genai import types

from ...errors import ExternalAIResponseError, ExternalAIUnavailableError

PROMPT_TEMPLATE = """
与えられた画像から、以下の情報を抽出して、出力形式に従ってJSON形式で出力してください。
出力はJSONオブジェクトのみ。コードフェンスや説明文などの余計な文字は一切付けないでください。


## 抽出する情報
- ブランド: Chumpion, Nikeなど
- カテゴリ: Tシャツ、スニーカーなど（以下のカテゴリ一覧から選択してください）

### カテゴリ一覧
{categories}

## 出力形式
{{
  "brand": "ブランド名",
  "category": "カテゴリ名",
  "retake_required": true or false,
  "retake_instructions": "ブランド名が写るようになど、**日本語**の再撮影の指示"
}}

### 出力例（成功時）
{{
  "brand": "Nike",
  "category": "スニーカー",
  "retake_required": false,
  "retake_instructions": ""
}}

### 出力例（再撮影が必要な場合）
{{
  "brand": "",
  "category": "スウェットシャツ",
  "retake_required": true,
  "retake_instructions": "スウェットシャツであることはわかりました。ブランド名が写るように再撮影してください"
}}
"""


class BaseInfoExtractor:
    """Run a Gemini prompt to extract basic product information from images."""

    def __init__(
        self,
        gemini_client: genai.Client,
        model="gemini-2.5-flash-lite",
        prompt_template: str = PROMPT_TEMPLATE,
    ):
        """基本情報抽出に必要なGeminiクライアント設定を初期化する。

        Args:
            gemini_client (genai.Client): Gemini APIクライアント。
            model (str): 利用するGeminiモデル名。
            prompt_template (str): 基本情報抽出用プロンプトテンプレート。
        """
        self.gemini_client = gemini_client
        self.model = model
        self.prompt_template = prompt_template

    def run(self, image_bytes: bytes, categories: list[str]) -> dict:
        """Extract brand/category and retake requirement from the given image."""
        prompt = self._construct_prompt(categories)
        try:
            response = self.gemini_client.models.generate_content(
                model=self.model,
                contents=[
                    types.Part.from_bytes(
                        data=image_bytes,
                        mime_type="image/png",
                    ),
                    prompt,
                ],
                config={
                    "response_mime_type": "application/json",
                },
            )
        except Exception as exc:
            raise ExternalAIUnavailableError("Base info extraction request failed") from exc

        try:
            if response.text is None:
                raise ExternalAIResponseError("Base info extraction returned empty response")
            return json.loads(response.text)
        except Exception as exc:
            raise ExternalAIResponseError("Base info extraction returned invalid JSON") from exc

    def _construct_prompt(self, categories: list[str]) -> str:
        """カテゴリのリストをプロンプト内のテーブル形式の文字列に変換する。

        Args:
            categories (list[str]): カテゴリ名のリスト。

        Returns:
            str: プロンプト内で使用するカテゴリ一覧の文字列。
        """
        category_lines = [f"- {category}" for category in categories]
        prompt = self.prompt_template.format(categories="\n".join(category_lines))
        return prompt
