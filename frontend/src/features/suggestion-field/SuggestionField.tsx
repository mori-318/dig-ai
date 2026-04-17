import type { SuggestionItem } from "../../types/suggestion"
import {
  clearValidationMessage,
  setRequiredValidationMessage,
} from "../form-field/validityHandlers"

type SuggestionFieldProps = {
  label: string
  value: string
  placeholder: string
  required?: boolean
  suggestions: SuggestionItem[]
  shouldShow: boolean
  onOpen: () => void
  onClose: () => void
  onChange: (value: string) => void
  onSelect: (value: string) => void
}

function SuggestionField({
  label,
  value,
  placeholder,
  required = false,
  suggestions,
  shouldShow,
  onOpen,
  onClose,
  onChange,
  onSelect,
}: SuggestionFieldProps) {
  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <div className="relative">
        <input
          className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
          type="text"
          required={required}
          value={value}
          onInvalid={setRequiredValidationMessage}
          onInput={clearValidationMessage}
          onFocus={onOpen}
          onBlur={() => setTimeout(onClose, 120)}
          onChange={(e) => {
            onChange(e.target.value)
            onOpen()
          }}
          placeholder={placeholder}
        />

        {shouldShow && (
          <ul className="absolute z-20 mt-1 max-h-56 w-full overflow-auto rounded-md border border-slate-200 bg-white py-1 text-sm shadow-lg">
            {suggestions.map((suggestion) => (
              <li key={suggestion.id}>
                <button
                  type="button"
                  className="block w-full px-3 py-2 text-left text-slate-700 hover:bg-slate-100"
                  onMouseDown={(e) => e.preventDefault()}
                  onClick={() => {
                    onSelect(suggestion.name)
                    onClose()
                  }}
                >
                  {suggestion.name}
                </button>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

export default SuggestionField
