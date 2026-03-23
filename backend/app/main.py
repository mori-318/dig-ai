from dotenv import load_dotenv
from fastapi import FastAPI

from .api.appraisal_router import router as appraisal_router

load_dotenv()

app = FastAPI()
app.include_router(appraisal_router)

@app.get("/")
async def root():
    return {
        "app-name": "Dig AI",
        "summary": "古着の画像を撮って、査定を行う"
    }
