import uuid

from .appraisal_state_store import AppraisalStateStore
from fastapi import UploadFile

from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult


class AppraisalService:
    def __init__(self, state_store: AppraisalStateStore, appraisal_agent) -> None:
        self.state_store = state_store

    def _new_appraisal_id(self) -> str:
        return str(uuid.uuid4())

    def start_appraisal(self, image: UploadFile) -> AppraisalResponse:
        appraisal_id = self._new_appraisal_id()
