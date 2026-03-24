import re

from ...agents.client import create_gemini_client
from .appraiser import Appraiser
from .base_info_extractor import BaseInfoExtractor


class AppraisalAgent:
    def __init__(self, item_info_tool):
        self.item_info_tool = item_info_tool
        self.gemini_client = create_gemini_client()
        self.base_info_extractor = BaseInfoExtractor(self.gemini_client)
        self.appraiser = Appraiser(self.gemini_client)

    def run(self, appraisal_id: str, image_bytes: bytes) -> dict:
        # 画像からブランド・カテゴリを抽出
        base_info_result = self.base_info_extractor.run(image_bytes)

        if base_info_result["retake_required"]:
            return {
                "status": "retake_required",
                "appraisal_id": appraisal_id,
                "retake_message": base_info_result["retake_instructions"],
                "retake_required_by": "base_info",
            }

        # 類似商品をツールから取得
        similar_items = self.item_info_tool(
            brand=base_info_result["brand"],
            category=base_info_result["category"],
        )

        # 画像と類似商品情報から査定を実行
        appraisal_result = self.appraiser.run(
            similar_item_descriptions=similar_items,
            image_bytes=image_bytes,
        )

        price_text = appraisal_result.get("appraisal_price", "")
        price_digits = re.sub(r"[^\d]", "", price_text)
        price = int(price_digits) if price_digits else 0

        return {
            "status": "done",
            "appraisal_id": appraisal_id,
            "result": {
                "appraisal_price": price,
                "appraisal_reason": appraisal_result.get("appraisal_reason", ""),
            },
        }
