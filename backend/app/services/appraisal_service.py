import uuid

from fastapi import UploadFile

from ..agents import AppraisalAgent
from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult


class AppraisalService:
    def __init__(self, appraisal_agent: AppraisalAgent) -> None:
        self.appraisal_agent = appraisal_agent

    def _new_appraisal_id(self) -> str:
        return str(uuid.uuid4())

    def start_appraisal(self, image: UploadFile) -> AppraisalResponse:
        """画像を受け取って、査定を行う

        Args:
            image (UploadFile): 査定対象の画像
        Returns:
            AppraisalResponse: 査定結果
        """
        appraisal_id = self._new_appraisal_id()

        image_bytes = image.file.read()
        appraisal_result = self.appraisal_agent.run(appraisal_id, image_bytes)

        if appraisal_result["status"] == "done":
            return AppraisalResponse(
                status=appraisal_result["status"],
                appraisal_id=appraisal_id,
                result=AppraisalResult(
                    brand=appraisal_result["result"]["brand"],
                    category=appraisal_result["result"]["category"],
                    appraisal_price=appraisal_result["result"]["appraisal_price"],
                    appraisal_reason=appraisal_result["result"]["appraisal_reason"],
                ),
            )
        else:
            return AppraisalResponse(
                status=appraisal_result["status"],
                appraisal_id=appraisal_id,
                retake_message=appraisal_result["retake_message"],
                retake_required_by=appraisal_result["retake_required_by"],
            )
