from pydantic import BaseModel, Field


class CreateAdminItemRequest(BaseModel):
    """管理者向けアイテム作成リクエスト。"""

    brand: str = Field(..., min_length=1, max_length=255)
    category: str = Field(..., min_length=1, max_length=255)
    name: str = Field(..., min_length=1, max_length=255)
    features_text: str
    appraisal_text: str
    price: int | None = None


class AdminItemResponse(BaseModel):
    """管理者向けアイテムレスポンス。"""

    id: int
    brand_id: int
    category_id: int
    name: str
    features_text: str | None
    appraisal_text: str | None
    price: int | None


class SuggestBrandRequest(BaseModel):
    """ブランドのサジェストリクエスト。"""

    q: str = Field(..., min_length=1, description="入力途中の検索文字列")


class Brand(BaseModel):
    """ブランド情報。"""

    id: int
    name: str


class CreateBrandRequest(BaseModel):
    """ブランド作成リクエスト。"""

    name: str = Field(..., min_length=1, max_length=255)


class SuggestBrandResponse(BaseModel):
    """ブランドのサジェストレスポンス。"""

    brands: list[Brand]


class SuggestCategoryRequest(BaseModel):
    """カテゴリーのサジェストリクエスト。"""

    q: str = Field(..., min_length=1, description="入力途中の検索文字列")


class Category(BaseModel):
    """カテゴリー情報。"""

    id: int
    name: str


class CreateCategoryRequest(BaseModel):
    """カテゴリ作成リクエスト。"""

    name: str = Field(..., min_length=1, max_length=255)


class SuggestCategoryResponse(BaseModel):
    """カテゴリーのサジェストレスポンス。"""

    categories: list[Category]
