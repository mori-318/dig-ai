from fastapi import APIRouter, Depends, File, UploadFile

from ..api.depends import get_appraisal_service
from ..schemas.appraisal_schemas import AppraisalResponse
from ..services.appraisal_service import AppraisalService

router = APIRouter(prefix="/appraisal", tags=["appraisal"])


@router.post("/", response_model=AppraisalResponse)
async def start_appraisal(
    item_image: UploadFile = File(...),
    appraisal_service: AppraisalService = Depends(get_appraisal_service),
) -> AppraisalResponse:
    return appraisal_service.run_appraisal(item_image)


@router.post("/{appraisal_id}/retake", response_model=AppraisalResponse)
async def retake_appraisal(
    appraisal_id: str,
    item_image: UploadFile = File(...),
    appraisal_service: AppraisalService = Depends(get_appraisal_service),
) -> AppraisalResponse:
    return appraisal_service.run_appraisal(item_image, appraisal_id=appraisal_id)
