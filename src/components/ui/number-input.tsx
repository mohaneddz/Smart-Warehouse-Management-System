import * as React from "react"
import { cn } from "@/lib/utils"

interface NumberInputProps extends Omit<React.InputHTMLAttributes<HTMLInputElement>, 'onChange'> {
  value: number
  onChange: (value: number) => void
  label?: string
  className?: string
  min?: number
  max?: number
  step?: number
  showLabel?: boolean
  integersOnly?: boolean
}

export function NumberInput({
  value,
  onChange,
  label,
  className,
  min,
  max,
  step = 1,
  showLabel = false,
  integersOnly = false,
  ...props
}: NumberInputProps) {
  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newValue = e.target.value === '' ? 0 : Number(e.target.value)
    if (!isNaN(newValue)) {
      const processedValue = integersOnly ? Math.floor(newValue) : newValue
      const clampedValue = min !== undefined ? Math.max(min, max ? Math.min(max, processedValue) : processedValue) : processedValue
      onChange(clampedValue)
    }
  }

  const increment = () => {
    const newValue = value + step
    if (!max || newValue <= max) {
      onChange(integersOnly ? Math.floor(newValue) : newValue)
    }
  }

  const decrement = () => {
    const newValue = value - step
    if (min === undefined || newValue >= min) {
      onChange(integersOnly ? Math.floor(newValue) : newValue)
    }
  }

  return (
    <div className={cn(
      "relative rounded-xl border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E] w-full",
      className
    )}>
      <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full px-2">
        <input
          type="number"
          value={value}
          onChange={handleInputChange}
          min={min}
          max={max}
          step={integersOnly ? 1 : step}
          className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          placeholder={label}
          aria-label={label}
          {...props}
        />
        <div className="grid grid-rows-2 gap-1">
          <button
            type="button"
            onClick={increment}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label={`Increase ${label || 'value'}`}
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              transform="rotate(-180)"
            >
              <path d="M8 8L0.205771 0H15.7942L8 8Z" fill="#8B939B" />
            </svg>
          </button>
          <button
            type="button"
            onClick={decrement}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label={`Decrease ${label || 'value'}`}
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="currentColor"
              xmlns="http://www.w3.org/2000/svg"
              transform="rotate(180)"
            >
              <path d="M8 0L15.7942 8H0.205771L8 0Z" fill="#8B939B" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  )
} 