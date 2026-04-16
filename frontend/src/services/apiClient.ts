import { apiBaseUrl } from "./apiBaseUrl"

type ApiErrorResponse = {
  detail?: string
}

async function buildErrorMessage(
  response: Response,
  fallbackMessage: string,
): Promise<string> {
  try {
    const data = (await response.json()) as ApiErrorResponse
    if (data?.detail) {
      return data.detail
    }
  } catch {
    // noop
  }
  return `${fallbackMessage} (${response.status})`
}

async function requestJson<T>(
  path: string,
  init: RequestInit,
  fallbackMessage: string,
): Promise<T> {
  const response = await fetch(`${apiBaseUrl}${path}`, init)
  if (!response.ok) {
    throw new Error(await buildErrorMessage(response, fallbackMessage))
  }
  return (await response.json()) as T
}

export async function postJson<TResponse>(
  path: string,
  payload: unknown,
  fallbackMessage: string,
): Promise<TResponse> {
  return requestJson<TResponse>(
    path,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    },
    fallbackMessage,
  )
}

export async function postFormData<TResponse>(
  path: string,
  formData: FormData,
  fallbackMessage: string,
): Promise<TResponse> {
  return requestJson<TResponse>(
    path,
    {
      method: "POST",
      body: formData,
    },
    fallbackMessage,
  )
}
