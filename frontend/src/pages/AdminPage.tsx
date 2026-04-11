import { useEffect, useMemo, useState, type FormEvent } from "react"

type ItemInfo = {
  brand: string
  category: string
  name: string
  featuresText: string
  appraisalText: string
  price: number | null
}

type BrandSuggestion = {
  id: number
  name: string
}

type SuggestBrandResponse = {
  brands: BrandSuggestion[]
}

const initialFormData: ItemInfo = {
  brand: "",
  category: "",
  name: "",
  featuresText: "",
  appraisalText: "",
  price: null,
}

function AdminPage() {
  const [formData, setFormData] = useState<ItemInfo>(initialFormData)
  const [brandSuggestions, setBrandSuggestions] = useState<BrandSuggestion[]>([])
  const [isBrandMenuOpen, setIsBrandMenuOpen] = useState(false)

  useEffect(() => {
    const q = formData.brand.trim()
    if (!q) {
      setBrandSuggestions([])
      return
    }

    const controller = new AbortController()
    const fetchSuggestions = async () => {
      try {
        const baseUrl = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000"
        const params = new URLSearchParams({ q, limit: "10" })
        const res = await fetch(`${baseUrl}/admin/items/brands/suggest?${params.toString()}`, {
          signal: controller.signal,
        })

        if (!res.ok) {
          setBrandSuggestions([])
          return
        }

        const data = (await res.json()) as SuggestBrandResponse
        setBrandSuggestions(data.brands ?? [])
      } catch {
        setBrandSuggestions([])
      }
    }

    fetchSuggestions()
    return () => controller.abort()
  }, [formData.brand])

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
  }

  const shouldShowBrandMenu = useMemo(
    () => isBrandMenuOpen && formData.brand.trim().length > 0 && brandSuggestions.length > 0,
    [isBrandMenuOpen, formData.brand, brandSuggestions.length],
  )

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      <header className="mx-auto mb-6 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-slate-700">管理者ページ</h1>
        <p className="mt-2 text-sm text-slate-500">古着情報を入力して登録できます。</p>
      </header>
      <hr className="mx-auto mb-6 w-full max-w-3xl border-0 border-t border-slate-300" />
      <form
        onSubmit={handleSubmit}
        className="mx-auto w-full max-w-3xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        <div className="grid gap-5 md:grid-cols-2">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">Brand</label>
            <div className="relative">
              <input
                className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
                type="text"
                value={formData.brand}
                onFocus={() => setIsBrandMenuOpen(true)}
                onBlur={() => setTimeout(() => setIsBrandMenuOpen(false), 120)}
                onChange={(e) => {
                  setFormData({ ...formData, brand: e.target.value })
                  setIsBrandMenuOpen(true)
                }}
                placeholder="例: Levi's"
              />

              {shouldShowBrandMenu && (
                <ul className="absolute z-20 mt-1 max-h-56 w-full overflow-auto rounded-md border border-slate-200 bg-white py-1 text-sm shadow-lg">
                  {brandSuggestions.map((brand) => (
                    <li key={brand.id}>
                      <button
                        type="button"
                        className="block w-full px-3 py-2 text-left text-slate-700 hover:bg-slate-100"
                        onMouseDown={(e) => e.preventDefault()}
                        onClick={() => {
                          setFormData({ ...formData, brand: brand.name })
                          setIsBrandMenuOpen(false)
                        }}
                      >
                        {brand.name}
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">Category</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              type="text"
              value={formData.category}
              onChange={(e) => setFormData({ ...formData, category: e.target.value })}
              placeholder="例: denim jacket"
            />
          </div>
        </div>

        <div className="mt-5 space-y-2">
          <label className="text-sm font-medium text-slate-700">Name</label>
          <input
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            type="text"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="商品名を入力"
          />
        </div>

        <div className="mt-5 space-y-2">
          <label className="text-sm font-medium text-slate-700">Features Text</label>
          <textarea
            className="min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            value={formData.featuresText}
            onChange={(e) => setFormData({ ...formData, featuresText: e.target.value })}
            placeholder="商品の特徴を記載"
          />
        </div>

        <div className="mt-5 space-y-2">
          <label className="text-sm font-medium text-slate-700">Appraisal Text</label>
          <textarea
            className="min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            value={formData.appraisalText}
            onChange={(e) => setFormData({ ...formData, appraisalText: e.target.value })}
            placeholder="査定コメントを記載"
          />
        </div>

        <div className="mt-5 space-y-2">
          <label className="text-sm font-medium text-slate-700">Price</label>
          <input
            className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
            type="number"
            value={formData.price ?? ""}
            onChange={(e) =>
              setFormData({
                ...formData,
                price: e.target.value ? parseFloat(e.target.value) : null,
              })
            }
            placeholder="0"
          />
        </div>

        <div className="mt-7 flex justify-end">
          <button
            type="submit"
            className="rounded-md bg-slate-700 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800"
          >
            Submit
          </button>
        </div>
      </form>
    </div>
  )
}

export default AdminPage
