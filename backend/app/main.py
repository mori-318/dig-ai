from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request

from .agents.appraisal_agent import AppraisalAgent
from .agents.tools.find_similar_items import build_find_similar_items_tool
from .api.appraisal_router import router as appraisal_router
from .infra.db import create_mysql_client, create_redis_client
from .repositories.brand_repository import BrandRepository
from .repositories.category_repository import CategoryRepository
from .repositories.item_repository import ItemRepository

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """アプリケーションのライフサイクルイベントを管理するためのコンテキストマネージャー。"""
    # 起動時
    app.state.redis_client = create_redis_client()
    app.state.mysql_client = create_mysql_client()
    item_repository = ItemRepository(app.state.mysql_client)
    brand_repository = BrandRepository(app.state.mysql_client)
    category_repository = CategoryRepository(app.state.mysql_client)
    find_similar_items_tool = build_find_similar_items_tool(
        item_repository=item_repository,
        brand_repository=brand_repository,
        category_repository=category_repository,
    )
    app.state.appraisal_agent = AppraisalAgent(find_similar_items=find_similar_items_tool)

    yield
    app.state.redis_client.close()
    app.state.mysql_client.close()


app = FastAPI(lifespan=lifespan)
app.include_router(appraisal_router)


@app.get("/")
async def root():
    """アプリケーションの基本情報を返すエンドポイント。"""
    return {"app-name": "Dig AI", "summary": "古着の画像を撮って、AI査定を行うアプリです。"}
