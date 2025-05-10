import { cn } from "@/lib/utils"

interface BooleanInputProps {
  value: boolean
  onChange: (value: boolean) => void
  label?: string
  className?: string
  disabled?: boolean
  showLabel?: boolean
}

export function BooleanInput({
  value,
  onChange,
  label,
  className,
  disabled = false,
  showLabel = false,
}: BooleanInputProps) {
  return (
    <div className={cn("flex items-center gap-2", className)}>
      {showLabel && label && (
        <label className="text-sm text-gray-400">{label}</label>
      )}
      <button
        type="button"
        role="switch"
        aria-checked={value}
        aria-label={label || "Toggle"}
        disabled={disabled}
        onClick={() => onChange(!value)}
        className={cn(
          "relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 focus-visible:ring-offset-background",
          value ? "bg-blue-600" : "bg-gray-700",
          disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"
        )}
      >
        <span
          className={cn(
            "inline-block h-4 w-4 transform rounded-full bg-white transition-transform",
            value ? "translate-x-6" : "translate-x-1"
          )}
        />
      </button>
    </div>
  )
} 