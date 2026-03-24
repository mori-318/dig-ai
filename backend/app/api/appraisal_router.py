from fastapi import APIRouter, Depends, File, UploadFile
from redis import Redis

from ..agents.appraisal_agent import AppraisalAgent
from ..api.depends import get_appraisal_agent, get_redis_client
from ..schemas.appraisal_schemas import AppraisalResponse, AppraisalResult

router = APIRouter(prefix="/appraisal", tags=["appraisal"])


@router.post("/")
async def start_appraisal(
    item_image: UploadFile = File(...),
    redis_client: Redis = Depends(get_redis_client),
    appraisal_agent: AppraisalAgent = Depends(get_appraisal_agent),
) -> AppraisalResponse:
    return AppraisalResponse(
        status="retake_required",
        appraisal_id="12345",
        retake_message="ブランドタグが見えるように、もう一度撮影してください。",
        retake_required_by="base_info",
    )


@router.post("/{appraisal_id}/retake")
async def retake_appraisal(
    appraisal_id: str, item_image: UploadFile = File(...), redis_client=Depends(get_redis_client)
) -> AppraisalResponse:
    return AppraisalResponse(
        status="done",
        appraisal_id=appraisal_id,
        result=AppraisalResult(
            appraisal_price=13500,
            appraisal_reason="査定例のダミー理由です。",
        ),
    )
