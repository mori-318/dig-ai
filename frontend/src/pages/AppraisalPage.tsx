import React, { useState } from 'react'
import { postFormData } from '../services/apiClient'

type AppraisalResponse = {
  status: 'done' | 'retake_required'
  appraisal_id: string
  result?: {
    brand: string
    category: string
    appraisal_price: number
    appraisal_reason: string
  }
  retake_message?: string
  retake_required_by?: 'base_info' | 'appraiser'
}

function AppraisalPage() {
  const [targetImage, setTargetImage] = useState<string | null>(null)
  const [targetFile, setTargetFile] = useState<File | null>(null)
  const [result, setResult] = useState<AppraisalResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleInputFile = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    setTargetFile(file)

    const reader = new FileReader()
    reader.onload = () => {
      setTargetImage(reader.result as string)
    }
    reader.readAsDataURL(file)
  }

  const handleSubmit = async () => {
    if (!targetFile) return
    setLoading(true)
    setError(null)

    try {
      const form = new FormData()
      form.append('item_image', targetFile)

      const data = await postFormData<AppraisalResponse>(
        '/appraisal/',
        form,
        '査定リクエストに失敗しました',
      )
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to submit appraisal.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-50 px-4 py-10">
      <header className="mx-auto mb-6 w-full max-w-3xl">
        <h1 className="text-3xl font-bold text-slate-700">査定ページ（プロトタイプのため、撮影機能なし）</h1>
        <p className="mt-2 text-sm text-slate-500">写真をアップロードして査定を開始します。</p>
      </header>
      <hr className="mx-auto mb-6 w-full max-w-3xl border-0 border-t border-slate-300" />

      <form
        onSubmit={(e) => {
          e.preventDefault()
          void handleSubmit()
        }}
        className="mx-auto w-full max-w-3xl rounded-xl border border-slate-200 bg-white p-6 shadow-sm"
      >
        <label className="block text-sm font-medium text-slate-700" htmlFor="item-image">
          画像アップロード
        </label>
        <input
          id="item-image"
          type="file"
          onChange={handleInputFile}
          accept="image/png,image/jpeg"
          className="mt-2 block w-full rounded-md border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 file:mr-3 file:rounded-md file:border-0 file:bg-slate-700 file:px-3 file:py-2 file:text-sm file:font-semibold file:text-white hover:file:bg-slate-800"
        />

        {targetImage && (
          <div className="mt-5">
            <p className="mb-2 text-sm text-slate-600">プレビュー</p>
            <img
              src={targetImage}
              alt="preview"
              className="max-h-72 w-auto rounded-lg border border-slate-200 object-contain"
            />
          </div>
        )}

        <div className="mt-7 flex justify-end">
          <button
            type="submit"
            disabled={!targetFile || loading}
            className="rounded-md bg-slate-700 px-5 py-2 text-sm font-semibold text-white transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-60"
          >
            {loading ? '査定中...' : '査定開始'}
          </button>
        </div>

        {error && <p className="mt-4 text-sm text-red-600">{error}</p>}

        {result && (
          <div className="mt-6 rounded-lg border border-slate-200 bg-slate-50 p-4">
            <h2 className="text-sm font-semibold text-slate-700">査定結果</h2>
            <pre className="mt-2 overflow-x-auto text-xs text-slate-700">
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>
        )}
      </form>
    </div>
  )
}

export default AppraisalPage
