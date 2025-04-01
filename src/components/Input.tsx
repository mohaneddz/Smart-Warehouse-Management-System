'use client';

import { useState, type ChangeEvent } from 'react';
import { cn } from '@/lib/utils';

interface QuantityInputProps {
  defaultValue?: number;
  step?: number;
  onChange?: (value: number) => void;
  className?: string;
}

function Input_field(
  props: any,
  { defaultValue = 1, step = 1, onChange, className }: QuantityInputProps,
) {
  const [value, setValue] = useState(defaultValue);

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    const newValue = Number.parseInt(e.target.value, 10);
    if (!isNaN(newValue) || e.target.value === '') {
      // Allow empty input or valid numbers
      const updatedValue = e.target.value === '' ? '' : newValue;
      setValue(updatedValue as any);
      if (typeof updatedValue === 'number') {
        onChange?.(updatedValue);
      }
    }
  };

  const increment = () => {
    const newValue = typeof value === 'number' ? value + step : step;
    setValue(newValue);
    onChange?.(newValue);
  };

  const decrement = () => {
    const newValue = typeof value === 'number' ? value - step : -step;
    setValue(newValue);
    onChange?.(newValue);
  };

  return (
    <div className=" relative rounded-xl border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E]">
      <div
        className={cn(
          ' w-75 flex items-center justify-between bg-[#10121E]  opacity-80 rounded-xl ',
          className,
        )}
      >
        <input
          type="text"
          value={value}
          onChange={handleInputChange}
          className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3"
          placeholder={props.text}
          aria-label="Quantity"
        />
        <div className="absolute right-4 flex flex-col gap-1">
          <button
            type="button"
            onClick={increment}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label="Increase quantity"
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M8 0L15.7942 8H0.205771L8 0Z" fill="currentColor" />
            </svg>
          </button>
          <button
            type="button"
            onClick={decrement}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label="Decrease quantity"
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path d="M8 8L0.205771 0H15.7942L8 8Z" fill="currentColor" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
export default Input_field;
