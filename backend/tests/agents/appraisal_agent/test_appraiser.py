from dotenv import load_dotenv
from app.agents.appraisal_agent.appraiser import Appraiser
from app.agents.client import create_gemini_client
from tests.conftest import SWEATSHIRT_IMAGE_PATH

load_dotenv()

similar_item_descriptions = [
    (
        "胸元に大きなロゴがプリントされている",
        "胸元にしっかりロゴがあると価格が高くなりやすい。また、全体的に保存状態が良くて、年代も2000年代初頭のモデルであるため、相場の中間価格よりやや高めの査定が妥当と判断した。",
        10000,
    ),
    (
        "1970〜80年代前半製造。タグが赤・青など単色表記。希少性が高いヴィンテージ個体。",
        "1970年代の製造で、また、サイズがXLと大きめであることから、希少性がかなり高い",
        15000,
    ),
    (
        "2020年代に中国で大量生産されたモデル。",
        "2020年代に大量生産された廉価版モデルであり、また、裾のリブが伸びている、色褪せなど全体的に保存状態があまり良くないことから、相場の中間価格よりかなり安めの査定が妥当と判断した。",
        1500,
    ),
]


def test_appraiser_with_sweatshirt_image():
    gemini_client = create_gemini_client()
    appraiser = Appraiser(gemini_client=gemini_client)

    with open(SWEATSHIRT_IMAGE_PATH, "rb") as f:
        image_bytes = f.read()

    result = appraiser.run(
        similar_item_descriptions=similar_item_descriptions, image_bytes=image_bytes
    )
    print(result)

    assert "appraisal_reason" in result
    assert "appraisal_price" in result
