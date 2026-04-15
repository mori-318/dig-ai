import uuid

from fastapi import UploadFile

from ..agents import AppraisalAgent
from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult


class AppraisalService:
    def __init__(self, appraisal_agent: AppraisalAgent) -> None:
        self.appraisal_agent = appraisal_agent

    def _new_appraisal_id(self) -> str:
        return str(uuid.uuid4())

    def _build_response(self, appraisal_id: str, appraisal_result: dict) -> AppraisalResponse:
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
        return AppraisalResponse(
            status=appraisal_result["status"],
            appraisal_id=appraisal_id,
            retake_message=appraisal_result["retake_message"],
            retake_required_by=appraisal_result["retake_required_by"],
        )

    def run_appraisal(self, image: UploadFile, appraisal_id: str | None = None) -> AppraisalResponse:
        """画像を受け取って査定を実行する。

        appraisal_id が未指定なら新規査定としてIDを発行し、
        指定されていれば既存査定IDで再実行する。
        """
        if appraisal_id is None:
            appraisal_id = self._new_appraisal_id()
        image_bytes = image.file.read()
        appraisal_result = self.appraisal_agent.run(appraisal_id, image_bytes)
        return self._build_response(appraisal_id, appraisal_result)
