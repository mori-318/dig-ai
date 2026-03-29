from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..api.depends import get_admin_item_service
from ..schemas.admin_item_schemas import (
    AdminItemResponse,
    Brand,
    Category,
    CreateAdminItemRequest,
    CreateBrandRequest,
    CreateCategoryRequest,
    SuggestBrandResponse,
    SuggestCategoryResponse,
)
from ..services.admin_item_service import AdminItemService

router = APIRouter(prefix="/admin/items", tags=["admin_items"])


@router.post("/", response_model=AdminItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    payload: CreateAdminItemRequest,
    admin_item_service: AdminItemService = Depends(get_admin_item_service),
):
    """管理者が古着アイテム情報を新規作成する。"""
    try:
        item = admin_item_service.create_item(**payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e
    return AdminItemResponse(**item)


@router.get("/brands/suggest", response_model=SuggestBrandResponse)
async def suggest_brands(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=50),
    admin_item_service: AdminItemService = Depends(get_admin_item_service),
):
    """入力途中のブランド名から候補を返す。"""
    brands = admin_item_service.suggest_brands(q=q, limit=limit)
    return SuggestBrandResponse(brands=brands)


@router.post("/brands", response_model=Brand, status_code=status.HTTP_201_CREATED)
async def create_brand(
    payload: CreateBrandRequest,
    admin_item_service: AdminItemService = Depends(get_admin_item_service),
):
    """ブランドを新規作成する。"""
    try:
        return admin_item_service.create_brand(payload.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e


@router.get("/categories/suggest", response_model=SuggestCategoryResponse)
async def suggest_categories(
    q: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=50),
    admin_item_service: AdminItemService = Depends(get_admin_item_service),
):
    """入力途中のカテゴリ名から候補を返す。"""
    categories = admin_item_service.suggest_categories(q=q, limit=limit)
    return SuggestCategoryResponse(categories=categories)


@router.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CreateCategoryRequest,
    admin_item_service: AdminItemService = Depends(get_admin_item_service),
):
    """カテゴリを新規作成する。"""
    try:
        return admin_item_service.create_category(payload.name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e)) from e
