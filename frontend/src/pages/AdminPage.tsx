import { useState, type FormEvent } from "react"
import { useSuggestions } from "../features/suggestion-field/useSuggestions"
import SuggestionField from "../features/suggestion-field/SuggestionField"
import TextField from "../features/form-field/TextField"
import TextareaField from "../features/form-field/TextareaField"

type ItemInfo = {
  brand: string
  category: string
  name: string
  featuresText: string
  appraisalText: string
  price: string
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

  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
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
            label="Brand"
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
            label="Category"
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
          label="Name"
          value={formData.name}
          placeholder="商品名を入力"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, name: value }))}
        />

        <TextareaField
          label="Features Text"
          value={formData.featuresText}
          placeholder="商品の特徴を記載"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, featuresText: value }))}
        />

        <TextareaField
          label="Appraisal Text"
          value={formData.appraisalText}
          placeholder="査定コメントを記載"
          required
          onChange={(value) => setFormData((prev) => ({ ...prev, appraisalText: value }))}
        />

        <TextField
          label="Price"
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
