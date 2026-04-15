import React, { useState } from 'react'
import { apiBaseUrl } from '../services/apiBaseUrl'

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

      const res = await fetch(`${apiBaseUrl}/appraisal/`, {
        method: 'POST',
        body: form,
      })

      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`)
      const data: AppraisalResponse = await res.json()
      setResult(data)
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Failed to submit appraisal.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <input
        type="file"
        onChange={handleInputFile}
        accept="image/png,image/jpeg"
      />
      <button onClick={handleSubmit} disabled={!targetFile || loading}>
        {loading ? '査定中...' : '査定開始'}
      </button>

      {targetImage && <img src={targetImage} alt="preview" style={{ maxWidth: 240 }} />}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {result && <pre>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  )
}

export default AppraisalPage
