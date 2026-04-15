from datetime import datetime
from typing import Literal, TypedDict


class ItemRecord(TypedDict):
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
    features_text: str | None
    appraisal_text: str | None
    price: int | None


class AppraisalResultPayload(TypedDict):
    brand: str
    category: str
    appraisal_price: int
    appraisal_reason: str


class DoneAppraisalResult(TypedDict):
    status: Literal["done"]
    appraisal_id: str
    result: AppraisalResultPayload


class RetakeRequiredAppraisalResult(TypedDict):
    status: Literal["retake_required"]
    appraisal_id: str
    retake_message: str
    retake_required_by: Literal["base_info", "appraiser"]


ServiceAppraisalResult = DoneAppraisalResult | RetakeRequiredAppraisalResult
