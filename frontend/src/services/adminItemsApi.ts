import { getJson, postJson } from "./apiClient"
import type { SuggestionItem, SuggestionType } from "../types/suggestion"

type SuggestBrandResponse = {
  brands: SuggestionItem[]
}

type SuggestCategoryResponse = {
  categories: SuggestionItem[]
}

type CreateAdminItemPayload = {
  brand: string
  category: string
  name: string
  features_text: string
  appraisal_text: string
  price: number | null
}

export type AdminItemResponse = {
  id: number
  brand_id: number
  category_id: number
  name: string
  features_text: string | null
  appraisal_text: string | null
  price: number | null
}

export async function fetchSuggestions(
  query: string,
  type: SuggestionType,
  limit = 20,
): Promise<SuggestionItem[]> {
  const queryTrimmed = query.trim()
  if (!queryTrimmed) {
    return []
  }

  const params = new URLSearchParams({
    q: queryTrimmed,
    limit: String(limit),
  })

  const data = await getJson<SuggestBrandResponse | SuggestCategoryResponse>(
    `/admin/items/${type}/suggest?${params.toString()}`,
    "候補の取得に失敗しました",
  )

  if (type === "brands" && "brands" in data) {
    return data.brands ?? []
  }
  if (type === "categories" && "categories" in data) {
    return data.categories ?? []
  }
  return []
}

export async function createAdminItem(
  payload: CreateAdminItemPayload,
): Promise<AdminItemResponse> {
  return postJson<AdminItemResponse>(
    "/admin/items/",
    payload,
    "送信に失敗しました",
  )
}
