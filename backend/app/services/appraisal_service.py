import uuid

from fastapi import UploadFile

from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult
from .appraisal_state_manager import AppraisalStateManager


class AppraisalService:
    def __init__(self, state_manager: AppraisalStateManager, appraisal_agent) -> None:
        self.state_manager = state_manager

    def _new_appraisal_id(self) -> str:
        return str(uuid.uuid4())

    def start_appraisal(self, image: UploadFile) -> AppraisalResponse:
        appraisal_id = self._new_appraisal_id()
