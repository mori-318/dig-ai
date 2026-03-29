"""管理者の追加した商品情報を、DBに格納する前に清書するエージェント。"""

import json

from ...agents.client import create_gemini_client

PROMPT_TEMPLATE = """
以下のfeature_textとappraisal_textを、改善の観点に従って改善し、出力して

## feature_text
{feature_text}

## appraisal_text
{appraisal_text}

## 改善の観点
- 誤字脱字がないか
- 日本語として自然か
- 簡潔な文章で、箇条書きになっているか

## 出力形式
以下のJSON形式で、改善されたfeature_textとappraisal_textを出力してください。
{{
    "normalized_feature_text": "改善されたfeature_text **日本語**",
    "normalized_appraisal_text": "改善されたappraisal_text **日本語**"
}}

## 出力例
{{
    "normalized_feature_text": "- 強いテーパートシルエットが特徴的\n- 裾部分が広い\n- 膝部分が２重生地になっている",
    "normalized_appraisal_text": "- 裾にほつれありがあるため、状態は「やや傷あり」\n- ブランドは有名で人気も高いため、相場は高め\n- ただし、色はあまり人気の色ではないため、相場よりやや低めの値段設定"
}}

"""


class ItemTextNormalizerAgent:
    """管理者の追加した商品情報を、DBに格納する前に清書するエージェント。"""

    def __init__(self, model="gemini-2.5-flash-lite"):
        self.gemini_client = create_gemini_client()
        self.model = model

    def run(self, feature_text: str, appraisal_text: str) -> dict:
        """与えられたfeature_textとappraisal_textを、プロンプトの観点に従って改善する。

        Args:
            feature_text (str): 商品の特徴を表すテキスト。
            appraisal_text (str): 商品の査定理由を表すテキスト。
        Returns:
            dict: 改善されたfeature_textとappraisal_textを含む辞書。
                {
                    "normalized_feature_text": "改善されたfeature_text **日本語**",
                    "normalized_appraisal_text": "改善されたappraisal_text **日本語**"
                }
        """
        prompt = PROMPT_TEMPLATE.format(feature_text=feature_text, appraisal_text=appraisal_text)
        response = self.gemini_client.models.generate_content(
            model=self.model,
            contents=[prompt],
            config={
                "response_mime_type": "application/json",
            },
        )

        response = json.loads(response.text)

        result = {
            "normalized_feature_text": response.get("normalized_feature_text", ""),
            "normalized_appraisal_text": response.get("normalized_appraisal_text", ""),
        }
        return result
