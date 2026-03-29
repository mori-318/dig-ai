from dotenv import load_dotenv

from app.agents import ItemTextNormalizerAgent

load_dotenv()


def test_item_text_normalizer_agent():
    """ItemTextNormalizerAgentのrunメソッドが、与えられたfeature_textとappraisal_textを改善して返すことをテストする。"""
    agent = ItemTextNormalizerAgent()

    feature_text = "バックポケットにブランドのタグがついていて、また、全体的にシルエットが綺麗なもの。赤色が特徴的。"
    appraisal_text = "この商品は、状態が良く、ブランドも有名なため、高値で取引されています。特に、赤色のデザインが人気で、シルエットも綺麗なため、需要が高いです。"

    result = agent.run(feature_text=feature_text, appraisal_text=appraisal_text)

    print(result)

    assert "normalized_feature_text" in result and result["normalized_feature_text"] != ""
    assert "normalized_appraisal_text" in result and result["normalized_appraisal_text"] != ""
