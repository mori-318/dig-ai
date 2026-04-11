import { useState, type FormEvent } from "react"

type ItemInfo = {
  brand: string
  category: string
  name: string
  featuresText: string
  appraisalText: string
  price: number | null
}

const initialFormData: ItemInfo = {
  brand: '',
  category: '',
  name: '',
  featuresText: '',
  appraisalText: '',
  price: null
}

function AdminPage() {
  const [formData, setFormData] = useState<ItemInfo>(initialFormData)

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
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700">Brand</label>
            <input
              className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
              type="text"
              value={formData.brand}
              onChange={(e) => setFormData({ ...formData, brand: e.target.value })}
              placeholder="例: Levi's"
            />
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
                price: e.target.value ? parseFloat(e.target.value) : null
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
