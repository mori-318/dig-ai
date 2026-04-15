"""査定開始・再撮影APIのルーター。"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from ..api.depends import get_appraisal_service
from ..errors import ExternalAIError
from ..schemas.appraisal_schemas import AppraisalResponse
from ..services.appraisal_service import AppraisalService

router = APIRouter(prefix="/appraisal", tags=["appraisal"])


@router.post("/", response_model=AppraisalResponse)
async def start_appraisal(
    item_image: UploadFile = File(...),
    appraisal_service: AppraisalService = Depends(get_appraisal_service),
) -> AppraisalResponse:
    """Start a new appraisal for the uploaded image."""
    try:
        return appraisal_service.run_appraisal(item_image)
    except ExternalAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Appraisal service is temporarily unavailable",
        ) from exc


@router.post("/{appraisal_id}/retake", response_model=AppraisalResponse)
async def retake_appraisal(
    appraisal_id: str,
    item_image: UploadFile = File(...),
    appraisal_service: AppraisalService = Depends(get_appraisal_service),
) -> AppraisalResponse:
    """Re-run appraisal with a new image for an existing appraisal ID."""
    try:
        return appraisal_service.run_appraisal(item_image, appraisal_id=appraisal_id)
    except ExternalAIError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Appraisal service is temporarily unavailable",
        ) from exc
