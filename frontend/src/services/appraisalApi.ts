import { postFormData } from "./apiClient"

export type AppraisalResponse = {
  status: "done" | "retake_required"
  appraisal_id: string
  result?: {
    brand: string
    category: string
    appraisal_price: number
    appraisal_reason: string
  }
  retake_message?: string
  retake_required_by?: "base_info" | "appraiser"
}

export async function requestAppraisal(
  formData: FormData,
): Promise<AppraisalResponse> {
  return postFormData<AppraisalResponse>(
    "/appraisal/",
    formData,
    "査定リクエストに失敗しました",
  )
}
