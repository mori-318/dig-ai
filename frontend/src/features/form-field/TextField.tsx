type TextFieldProps = {
  label: string
  value: string
  placeholder?: string
  type?: "text" | "number"
  inputMode?: React.HTMLAttributes<HTMLInputElement>["inputMode"]
  onChange: (value: string) => void
}

function TextField({
  label,
  value,
  placeholder,
  type = "text",
  inputMode,
  onChange,
}: TextFieldProps) {
  return (
    <div className="mt-5 space-y-2">
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <input
        className="w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
        type={type}
        inputMode={inputMode}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  )
}

export default TextField
