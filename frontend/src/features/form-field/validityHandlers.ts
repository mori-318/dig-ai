import type { FormEvent, InvalidEvent } from "react"

type FormControlElement = HTMLInputElement | HTMLTextAreaElement

export function setRequiredValidationMessage(
  event: InvalidEvent<FormControlElement>,
): void {
  event.currentTarget.setCustomValidity("入力してください")
}

export function clearValidationMessage(event: FormEvent<FormControlElement>): void {
  event.currentTarget.setCustomValidity("")
}
