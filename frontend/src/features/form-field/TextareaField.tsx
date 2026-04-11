type TextareaFieldProps = {
  label: string
  value: string
  placeholder?: string
  onChange: (value: string) => void
}

function TextareaField({ label, value, placeholder, onChange }: TextareaFieldProps) {
  return (
    <div className="mt-5 space-y-2">
      <label className="text-sm font-medium text-slate-700">{label}</label>
      <textarea
        className="min-h-24 w-full rounded-md border border-slate-300 px-3 py-2 text-sm outline-none transition focus:border-slate-500 focus:ring-2 focus:ring-slate-200"
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
      />
    </div>
  )
}

export default TextareaField
