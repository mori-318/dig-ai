"""画像と類似商品情報から査定理由と価格を生成する処理。"""

import json

from google import genai
from google.genai import types

from ...errors import ExternalAIResponseError, ExternalAIUnavailableError

PROMPT_TEMPLATE = """
以下の特徴・観点と価格例を参考にして、与えられた画像の金額を鑑定してください。
その際、なぜそのような結果になるか、step by stepで考えてその考えも出力してください。

## 類似商品の特徴、査定理由、価格
{item_descriptions}

## 出力形式
以下のJSON形式で、画像から抽出すべき項目を出力してください。
{{
    "appraisal_reason": "step by stepで考えた査定の理由。***日本語*",
    "appraisal_price": 1000,
}}

## 出力例
{{
    "appraisal_reason": "価格例の参照: 「色が新品に近い場合は高め」とある。画像では発色が良く退色が少ないため、この観点は高評価寄り。\n価格例の参照: 「年代が古いほど限定性や歴史的価値で高価になることがある」とある。画像は古いモデルに見え、流通量も少なそうなので加点要素。\n価格例の参照: 「保存状態が良いほど減額が少ない」とある。目立つキズが見当たらず付属品も揃っているため、相場より上振れの可能性が高い。\n以上より、相場の中間価格よりやや高めの査定が妥当と判断した。",
    "appraisal_price": 1000
}}
"""


class Appraiser:
    """Run the appraisal step by prompting Gemini with similar item context."""

    def __init__(
        self,
        gemini_client: genai.Client,
        model="gemini-2.5-flash-lite",
        prompt_template: str = PROMPT_TEMPLATE,
    ):
        """査定実行に必要なGeminiクライアント設定を初期化する。

        Args:
            gemini_client (genai.Client): Gemini APIクライアント。
            model (str): 利用するGeminiモデル名。
            prompt_template (str): 査定用プロンプトテンプレート。
        """
        self.gemini_client = gemini_client
        self.model = model
        self.prompt_template = prompt_template

    def run(self, similar_item_descriptions: list, image_bytes: bytes) -> dict:
        """Estimate price and reason from an image and similar item descriptions."""
        prompt = self._construct_prompt(similar_item_descriptions)
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
            raise ExternalAIUnavailableError("Appraiser request failed") from exc

        try:
            if response.text is None:
                raise ExternalAIResponseError("Appraiser returned empty response")
            return json.loads(response.text)
        except Exception as exc:
            raise ExternalAIResponseError("Appraiser returned invalid JSON") from exc

    def _construct_prompt(self, similar_item_descriptions: list) -> str:
        """与えられた特徴、査定理由、価格のリストを、プロンプト内のテーブル形式の文字列に変換する。

        Args:
            similar_item_descriptions (list): 特徴、査定理由、価格のタプルのリスト。各要素は (特徴, 査定理由, 価格) の形式。
        Returns:
            str: モデルに与えるプロンプト。similar_item_descriptionsをマークダウンテーブル形式に変換してPROMPT_TEMPLATEに埋め込んだ文字列。
        """
        item_descriptions_str = "| No. | 特徴 | 査定理由 | 価格 |\n| --- | --- | --- | --- |\n"
        for idx, (feature_text, appraisal_text, price) in enumerate(
            similar_item_descriptions, start=1
        ):
            item_descriptions_str += f"| {idx} | {feature_text} | {appraisal_text} | {price}円 |\n"

        prompt = self.prompt_template.format(item_descriptions=item_descriptions_str)
        return prompt
