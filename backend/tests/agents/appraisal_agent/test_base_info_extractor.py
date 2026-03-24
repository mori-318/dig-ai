from dotenv import load_dotenv
from app.agents.appraisal_agent.base_info_extractor import BaseInfoExtractor
from app.agents.client import create_gemini_client
from tests.conftest import SWEATSHIRT_IMAGE_PATH, WHITE_WALL_IMAGE_PATH

load_dotenv()


def test_base_info_extractor_with_sweatshirt_image():
    """
    スウェットシャツの画像を入力として、ブランドが特定できない場合に再撮影の指示が含まれることを確認するテスト
    画像は、ブランド: GILDAN, カテゴリ: スウェットシャツ
    期待する出力:
        {
            "brand": "GILDAN",
            "category": "スウェットシャツ",
            "retake_required": false,
            "retake_instructions": ""
        }
    """
    extractor = BaseInfoExtractor(create_gemini_client())
    result = extractor.run(SWEATSHIRT_IMAGE_PATH.read_bytes())
    print(result)

    assert result["brand"].lower() == "gildan"
    assert result["category"] == "スウェットシャツ"
    assert result["retake_required"] == False
    assert result["retake_instructions"] == ""


def test_base_info_extractor_with_white_wall_image():
    """
    白い壁の画像を入力として、ブランド・カテゴリが特定できない場合の出力になっているかを確認するテスト
    期待する出力:
        {
            "brand": "",
            "category": "",
            "retake_required": true,
            "retake_instructions": "{何らかの、再撮影の指示}"
        }
    """
    extractor = BaseInfoExtractor(create_gemini_client())
    result = extractor.run(WHITE_WALL_IMAGE_PATH.read_bytes())
    print(result)

    assert result["brand"] == ""
    assert result["category"] == ""
    assert result["retake_required"] == True
    assert result["retake_instructions"].strip() != ""
