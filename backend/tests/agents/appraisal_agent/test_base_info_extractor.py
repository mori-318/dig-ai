from app.agents.appraisal_agent.base_info_extractor import BaseInfoExtractor


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


def test_construct_prompt_includes_categories():
    """カテゴリ一覧がプロンプトに埋め込まれること。"""
    client = DummyGeminiClient(
        '{"brand":"GILDAN","category":"スウェットシャツ","retake_required":false,"retake_instructions":""}'
    )
    extractor = BaseInfoExtractor(client)
    prompt = extractor._construct_prompt(["スウェットシャツ", "ジーンズ"])

    assert "- スウェットシャツ" in prompt
    assert "- ジーンズ" in prompt


def test_run_returns_parsed_json_and_passes_prompt():
    """runがJSONを辞書として返し、モデル呼び出しにカテゴリ入りプロンプトを渡すこと。"""
    response_text = (
        '{"brand":"GILDAN","category":"スウェットシャツ","retake_required":false,"retake_instructions":""}'
    )
    client = DummyGeminiClient(response_text)
    extractor = BaseInfoExtractor(client)

    result = extractor.run(b"dummy-image", ["スウェットシャツ", "ジーンズ"])

    assert result["brand"] == "GILDAN"
    assert result["category"] == "スウェットシャツ"
    assert result["retake_required"] is False
    assert result["retake_instructions"] == ""
    assert client.models.last_kwargs is not None
    contents = client.models.last_kwargs["contents"]
    assert any(isinstance(c, str) and "- スウェットシャツ" in c for c in contents)
