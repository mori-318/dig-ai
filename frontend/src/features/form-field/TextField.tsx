type TextFieldProps = {
  label: string
  value: string
  placeholder?: string
  type?: "text" | "number"
  inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"]
  required?: boolean
  onChange: (value: string) => void
}

function TextField({
  label,
  value,
  placeholder,
  type = "text",
  inputMode,
  required = false,
  onChange,
}: TextFieldProps) {
  return (
    <div className="mt-5 space-y-2">
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
        type={type}
        inputMode={inputMode}
        required={required}
        value={value}
        onInvalid={(e) => e.currentTarget.setCustomValidity("入力してください")}
        onInput={(e) => e.currentTarget.setCustomValidity("")}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  )
}

export default TextField
