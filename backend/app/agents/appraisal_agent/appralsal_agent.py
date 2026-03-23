from ...agents.client import create_gemini_client

from .base_info_extractor import BaseInfoExtractor

class AppraisalAgent:
    def __init__(self, item_info_tool):
        self.item_info_tool = item_info_tool
        self.gemini_client = create_gemini_client()
        self.base_info_extractor = BaseInfoExtractor(self.gemini_client)

    def run(self, image_bytes: bytes) -> dict:
        # 画像からブランド・カテゴリを抽出
        base_info = self.base_info_extractor.run(image_bytes)
        return base_info
