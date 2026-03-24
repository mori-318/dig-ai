from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class AppraisalResult(BaseModel):
    """査定結果モデル

    Attributes:
        brand: 査定されたブランド
        category: 査定されたカテゴリ
        appraisal_price: 査定された価格
        appraisal_reason: 査定理由
    """

    brand: str
    category: str
    appraisal_price: int
    appraisal_reason: str


class AppraisalResponse(BaseModel):
    """査定のレスポンスモデル

    Attributes:
        status: 査定のステータス。done: 査定完了、retake_required: 再撮影が必要
        appraisal_id: 査定ID
        result: 査定結果。statusがdoneのときに必須
        retake_message: 再撮影が必要な場合のメッセージ。statusがretake_requiredのときに必須
        retake_required_by: 再撮影が必要な場合の理由。
            base_info: ブランドタグなどの基本情報が不明瞭なため
            appraiser: 画像に査定に必要な情報が十分ではなく、再撮影が必要と判断したため
    """

    status: Literal["done", "retake_required"]
    appraisal_id: str
    result: Optional[AppraisalResult] = None
    retake_message: Optional[str] = None
    retake_required_by: Optional[Literal["base_info", "appraiser"]] = None

    @model_validator(mode="after")
    def validate_status(self) -> "AppraisalResponse":
        if self.status == "done":
            if self.result is None:
                raise ValueError("result is required when status is done")
            if self.retake_message is not None:
                raise ValueError("retake_message must be null when status is done")
            if self.retake_required_by is not None:
                raise ValueError("retake_required_by must be null when status is done")
        else:
            if self.result is not None:
                raise ValueError("result must be null when status is retake_required")
            if self.retake_message is None:
                raise ValueError("retake_message is required when status is retake_required")
            if self.retake_required_by is None:
                raise ValueError("retake_required_by is required when status is retake_required")
        return self
