from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from .api.appraisal_router import router as appraisal_router
from .container import build_appraisal_agent, build_appraisal_state_manager
from .infra.db import create_mysql_client, create_redis_client

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクルイベントを管理するためのコンテキストマネージャー。"""
    # 起動時
    app.state.redis_client = create_redis_client()
    app.state.mysql_client = create_mysql_client()
    app.state.appraisal_state_manager = build_appraisal_state_manager(app.state.redis_client)
    app.state.appraisal_agent = build_appraisal_agent(
        app.state.mysql_client,
        app.state.appraisal_state_manager,
    )

    yield
    app.state.redis_client.close()
    app.state.mysql_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(appraisal_router)


@app.get("/")
async def root():
    """アプリケーションの基本情報を返すエンドポイント。"""
    return {"app-name": "Dig AI", "summary": "古着の画像を撮って、AI査定を行うアプリです。"}
