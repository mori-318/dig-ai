from typing import Literal, Optional

from pydantic import BaseModel, model_validator


class AppraisalResult(BaseModel):
    appraisal_price: int
    appraisal_reason: str


class AppraisalResponse(BaseModel):
    status: Literal["done", "retake_required"]
    appraisal_id: str
    result: Optional[AppraisalResult] = None
    retake_message: Optional[str] = None
    retake_required_by: Optional[Literal["base_info", "detailed_info"]] = None

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
