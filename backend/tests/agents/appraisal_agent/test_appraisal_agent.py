from unittest.mock import MagicMock

import pytest

from app.agents import AppraisalAgent


@pytest.fixture
def state_manager():
    manager = MagicMock()
    manager.get.return_value = None
    return manager


def _build_agent(state_manager, find_similar_items):
    agent = AppraisalAgent(
        find_similar_items=find_similar_items,
        state_manager=state_manager,
    )
    agent.base_info_extractor.run = MagicMock()
    agent.appraiser.run = MagicMock()
    return agent


def test_run_done_flow(state_manager):
    """正常系の査定完了フローを検証する。"""
    find_similar_items = MagicMock(
        return_value=[{"features_text": "f", "appraisal_text": "a", "price": 1000}]
    )
    agent = _build_agent(state_manager, find_similar_items)
    agent.base_info_extractor.run.return_value = {
        "brand": "Brand A",
        "category": "Category X",
        "retake_required": False,
        "retake_instructions": "",
    }
    agent.appraiser.run.return_value = {
        "appraisal_price": "1000",
        "appraisal_reason": "理由",
    }

    result = agent.run("id-1", b"image")

    assert result["status"] == "done"
    assert result["result"]["brand"] == "Brand A"
    assert result["result"]["category"] == "Category X"
    assert result["result"]["appraisal_price"] == 1000
    assert result["result"]["appraisal_reason"] == "理由"
    state_manager.set.assert_called()
    state_manager.delete.assert_called_with("id-1")


def test_run_retake_required_at_base_info(state_manager):
    """base_infoで再撮影が必要な場合を検証する。"""
    find_similar_items = MagicMock()
    agent = _build_agent(state_manager, find_similar_items)
    agent.base_info_extractor.run.return_value = {
        "brand": "",
        "category": "Category X",
        "retake_required": True,
        "retake_instructions": "再撮影してください",
    }

    result = agent.run("id-2", b"image")

    assert result["status"] == "retake_required"
    assert result["retake_required_by"] == "base_info"
    assert "retake_message" in result
    find_similar_items.assert_not_called()
    agent.appraiser.run.assert_not_called()


def test_run_done_when_similar_items_empty(state_manager):
    """類似商品が空の場合の査定終了を検証する。"""
    find_similar_items = MagicMock(return_value=[])
    agent = _build_agent(state_manager, find_similar_items)
    agent.base_info_extractor.run.return_value = {
        "brand": "Brand A",
        "category": "Category X",
        "retake_required": False,
        "retake_instructions": "",
    }

    result = agent.run("id-3", b"image")

    assert result["status"] == "done"
    assert result["result"]["appraisal_price"] == -1
    assert "査定ができませんでした" in result["result"]["appraisal_reason"]
