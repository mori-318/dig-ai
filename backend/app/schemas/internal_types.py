"""リポジトリ層とサービス層で利用する内部型定義。"""

from datetime import datetime
from typing import Literal, TypedDict


class ItemRecord(TypedDict):
    """アイテムテーブル1件分のレコード型。"""

    id: int
    brand_id: int
    category_id: int
    name: str
    features_text: str | None
    appraisal_text: str | None
    price: int | None
    updated_at: datetime
    created_at: datetime


class SimilarItem(TypedDict):
    """査定時に参照する類似商品の要約情報。"""

    features_text: str | None
    appraisal_text: str | None
    price: int | None


class AppraisalResultPayload(TypedDict):
    """査定完了時に返す結果ペイロード。"""

    brand: str
    category: str
    appraisal_price: int
    appraisal_reason: str


class DoneAppraisalResult(TypedDict):
    """査定完了ステータス時のサービス戻り値型。"""

    status: Literal["done"]
    appraisal_id: str
    result: AppraisalResultPayload


class RetakeRequiredAppraisalResult(TypedDict):
    """再撮影要求ステータス時のサービス戻り値型。"""

    status: Literal["retake_required"]
    appraisal_id: str
    retake_message: str
    retake_required_by: Literal["base_info", "appraiser"]


ServiceAppraisalResult = DoneAppraisalResult | RetakeRequiredAppraisalResult


class BrandRecord(TypedDict):
    """ブランドテーブル1件分のレコード型。"""

    id: int
    name: str
    created_at: datetime


class CategoryRecord(TypedDict):
    """カテゴリテーブル1件分のレコード型。"""

    id: int
    name: str
    created_at: datetime


class CategoryListItem(TypedDict):
    """カテゴリ一覧表示向けの簡易レコード型。"""

    id: int
    name: str
