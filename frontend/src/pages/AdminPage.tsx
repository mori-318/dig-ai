import { useState, type FormEvent } from "react"
import { useSuggestions } from "../features/suggestion-field/useSuggestions"
import SuggestionField from "../features/suggestion-field/SuggestionField"
import TextField from "../features/form-field/TextField"
import TextareaField from "../features/form-field/TextareaField"
import { postJson } from "../services/apiClient"

type ItemInfo = {
  brand: string
  category: string
  name: string
  featuresText: string
  appraisalText: string
  price: string
}

type AdminItemResponse = {
  id: number
  brand_id: number
  category_id: number
  name: string
  features_text: string | null
  appraisal_text: string | null
  price: number | null
}

const initialFormData: ItemInfo = {
  brand: "",
  category: "",
  name: "",
  featuresText: "",
  appraisalText: "",
  price: "",
}

function AdminPage() {
  const [formData, setFormData] = useState<ItemInfo>(initialFormData)
  const [submitting, setSubmitting] = useState(false)
  const [submitError, setSubmitError] = useState<string | null>(null)
  const [submitSuccess, setSubmitSuccess] = useState<string | null>(null)
  const {
    suggestions: brandSuggestions,
    shouldShow: shouldShowBrandMenu,
    open: openBrandMenu,
    close: closeBrandMenu,
  } = useSuggestions(formData.brand, "brands", 10)

  const {
    suggestions: categorySuggestions,
    shouldShow: shouldShowCategoryMenu,
    open: openCategoryMenu,
    close: closeCategoryMenu,
  } = useSuggestions(formData.category, "categories", 10)

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()

    setSubmitError(null)
    setSubmitSuccess(null)

    const trimmedPrice = formData.price.trim()
    const parsedPrice = trimmedPrice === "" ? null : Number(trimmedPrice)
    if (trimmedPrice !== "" && !Number.isFinite(parsedPrice)) {
      setSubmitError("Priceは数値で入力してください")
      return
    }

    try {
      setSubmitting(true)
      await postJson<AdminItemResponse>(
        "/admin/items/",
        {
          brand: formData.brand.trim(),
          category: formData.category.trim(),
          name: formData.name.trim(),
          features_text: formData.featuresText.trim(),
          appraisal_text: formData.appraisalText.trim(),
          price: parsedPrice,
        },
        "送信に失敗しました",
      )

      setSubmitSuccess("登録しました")
      setFormData(initialFormData)
    } catch {
      setSubmitError("ネットワークエラーが発生しました")
    } finally {
      setSubmitting(false)
    }
  }

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
          <SuggestionField
            label="ブランド"
            value={formData.brand}
            placeholder="例: Levi's"
            required
            suggestions={brandSuggestions}
            shouldShow={shouldShowBrandMenu}
            onOpen={openBrandMenu}
            onClose={closeBrandMenu}
            onChange={(value) => setFormData((prev) => ({ ...prev, brand: value }))}
            onSelect={(value) => setFormData((prev) => ({ ...prev, brand: value }))}
          />
          <SuggestionField
            label="カテゴリー"
            value={formData.category}
            placeholder="例: denim jacket"
            required
            suggestions={categorySuggestions}
            shouldShow={shouldShowCategoryMenu}
            onOpen={openCategoryMenu}
            onClose={closeCategoryMenu}
            onChange={(value) => setFormData((prev) => ({ ...prev, category: value }))}
            onSelect={(value) => setFormData((prev) => ({ ...prev, category: value }))}
          />
        </div>

        <TextField
          label="アイテム名"
          value={formData.name}
          placeholder="商品名を入力"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, name: value }))}
        />

        <TextareaField
          label="このアイテムの特徴"
          value={formData.featuresText}
          placeholder="商品の特徴を記載"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, featuresText: value }))}
        />

        <TextareaField
          label="査定時のポイント"
          value={formData.appraisalText}
          placeholder="なぜこの価格になるのか、査定のポイントを記載"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, appraisalText: value }))}
        />

        <TextField
          label="価格 (円)"
          type="text"
          inputMode="numeric"
          value={formData.price}
          placeholder="0"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, price: value }))}
        />

        <div className="mt-7 flex justify-end">
          <button
            type="submit"
            disabled={submitting}
            className="rounded-md bg-slate-700 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {submitting ? "Submitting..." : "Submit"}
          </button>
        </div>

        {submitError && <p className="mt-4 text-sm text-red-600">{submitError}</p>}
        {submitSuccess && <p className="mt-4 text-sm text-green-600">{submitSuccess}</p>}
      </form>
    </div>
  )
}

export default AdminPage
