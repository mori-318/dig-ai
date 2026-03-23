from fastapi import APIRouter, UploadFile, File

from ..schemas.appraisal_schemas import AppraisalResult, AppraisalResponse

router = APIRouter(prefix="/appraisal", tags=["appraisal"])

@router.post("/")
async def start_appraisal(item_image: UploadFile = File(...)) -> AppraisalResponse:
    return AppraisalResponse(
        status="retake_required",
        appraisal_id="12345",
        retake_message="ブランドタグが見えるように、もう一度撮影してください。",
        retake_required_by="base_info"
    )

@router.post("/{appraisal_id}/retake")
async def retake_appraisal(appraisal_id: str, item_image: UploadFile = File(...)) -> AppraisalResponse:
    return AppraisalResponse(
        status="done",
        appraisal_id=appraisal_id,
        result=AppraisalResult(
            category="スウェットシャツ",
            brand="NIKE",
            price=13500,
            attributes={
                "サイズ": "L",
                "色": "黒",
                "年代": "1990年代"
            }
        )
    )
