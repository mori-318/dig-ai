from app.agents.appraisal_agent.appraiser import Appraiser


class DummyResponse:
    def __init__(self, text: str):
        self.text = text


class DummyModels:
    def __init__(self, text: str):
        self._text = text
        self.last_kwargs = None

    def generate_content(self, **kwargs):
        self.last_kwargs = kwargs
        return DummyResponse(self._text)


class DummyGeminiClient:
    def __init__(self, text: str):
        self.models = DummyModels(text)


def test_construct_prompt_contains_similar_items_table():
    """類似商品情報がテーブル形式でプロンプトに含まれること。"""
    client = DummyGeminiClient('{"appraisal_reason":"理由","appraisal_price":"1000円"}')
    appraiser = Appraiser(client)

    prompt = appraiser._construct_prompt(
        [
            ("胸元に大きなロゴ", "状態が良く高評価", 10000),
            ("色褪せあり", "使用感があり減額", 1500),
        ]
    )

    assert "| No. | 特徴 | 査定理由 | 価格 |" in prompt
    assert "胸元に大きなロゴ" in prompt
    assert "1500円" in prompt


def test_run_returns_parsed_json():
    """runがモデルレスポンスJSONを辞書として返すこと。"""
    client = DummyGeminiClient('{"appraisal_reason":"理由","appraisal_price":"1000円"}')
    appraiser = Appraiser(client)

    result = appraiser.run(
        similar_item_descriptions=[("特徴", "査定理由", 1000)],
        image_bytes=b"dummy-image",
    )

    assert result["appraisal_reason"] == "理由"
    assert result["appraisal_price"] == "1000円"
    assert client.models.last_kwargs is not None
