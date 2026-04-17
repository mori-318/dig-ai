import { useEffect, useMemo, useState } from "react"
import { fetchSuggestions } from "../../services/adminItemsApi"
import type { SuggestionItem, SuggestionType } from "../../types/suggestion"

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
    const loadSuggestions = async () => {
      try {
        const nextSuggestions = await fetchSuggestions(queryTrimmed, type, limit)
        if (!controller.signal.aborted) {
          setSuggestions(nextSuggestions)
        }
      } catch {
        if (!controller.signal.aborted) {
          setSuggestions([])
        }
      }
    }

    void loadSuggestions()
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
