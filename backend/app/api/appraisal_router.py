from fastapi import APIRouter, Depends, File, UploadFile
from redis import Redis

from ..agents import AppraisalAgent
from ..api.depends import get_appraisal_agent, get_redis_client
from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult
from ..services.appraisal_service import AppraisalService

router = APIRouter(prefix="/appraisal", tags=["appraisal"])


@router.post("/")
async def start_appraisal(
    item_image: UploadFile = File(...),
    appraisal_agent: AppraisalAgent = Depends(get_appraisal_agent),
) -> AppraisalResponse:
    service = AppraisalService(
        appraisal_agent=appraisal_agent,
    )
    return service.start_appraisal(item_image)


@router.post("/{appraisal_id}/retake")
async def retake_appraisal(
    appraisal_id: str, item_image: UploadFile = File(...), redis_client=Depends(get_redis_client)
) -> AppraisalResponse:
    return AppraisalResponse(
        status="done",
        appraisal_id=appraisal_id,
        result=AppraisalResult(
            brand="Brand A",
            category="Category X",
            appraisal_price=13500,
            appraisal_reason="査定例のダミー理由です。",
        ),
    )
