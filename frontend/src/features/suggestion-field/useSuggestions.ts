import { useEffect, useMemo, useState } from "react"
import { apiBaseUrl } from "../../services/apiBaseUrl"

export type SuggestionType = "brands" | "categories"

export type SuggestionItem = {
  id: number
  name: string
}

type SuggestBrandResponse = {
  brands: SuggestionItem[]
}

type SuggestCategoryResponse = {
  categories: SuggestionItem[]
}

type UseSuggestionsResult = {
  suggestions: SuggestionItem[]
  isOpen: boolean
  shouldShow: boolean
  open: () => void
  close: () => void
  setIsOpen: (value: boolean) => void
}

export function useSuggestions(
  query: string,
  type: SuggestionType,
  limit = 20,
): UseSuggestionsResult {
  const [suggestions, setSuggestions] = useState<SuggestionItem[]>([])
  const [isOpen, setIsOpen] = useState(false)
  const [debouncedQuery, setDebouncedQuery] = useState(query)

  useEffect(() => {
    const timer = window.setTimeout(() => {
      setDebouncedQuery(query)
    }, 300)
    return () => window.clearTimeout(timer)
  }, [query])

  useEffect(() => {
    const queryTrimmed = debouncedQuery.trim()
    if (!queryTrimmed) {
      setSuggestions([])
      return
    }

    const controller = new AbortController()
    const fetchSuggestions = async () => {
      try {
        const params = new URLSearchParams({ q: queryTrimmed, limit: String(limit) })
        const path = `/admin/items/${type}/suggest`
        const res = await fetch(`${apiBaseUrl}${path}?${params.toString()}`, { signal: controller.signal })
        if (!res.ok) {
          setSuggestions([])
          return
        }

        const data = (await res.json()) as SuggestBrandResponse | SuggestCategoryResponse
        if (type === "brands" && "brands" in data) {
          setSuggestions(data.brands ?? [])
          return
        }
        if (type === "categories" && "categories" in data) {
          setSuggestions(data.categories ?? [])
          return
        }
        setSuggestions([])
      } catch {
        setSuggestions([])
      }
    }

    void fetchSuggestions()
    return () => controller.abort()
  }, [debouncedQuery, limit, type])

  const shouldShow = useMemo(
    () => isOpen && debouncedQuery.trim().length > 0 && suggestions.length > 0,
    [debouncedQuery, isOpen, suggestions.length],
  )

  return {
    suggestions,
    isOpen,
    shouldShow,
    open: () => setIsOpen(true),
    close: () => setIsOpen(false),
    setIsOpen,
  }
}
