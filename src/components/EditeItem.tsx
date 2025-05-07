import React from 'react';

interface NumberInputProps {
  label: string;
  name: string;
  value: number;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onIncrement: (name: string) => void;
  onDecrement: (name: string) => void;
}

const NumberInput: React.FC<NumberInputProps> = ({
  label,
  name,
  value,
  onChange,
  onIncrement,
  onDecrement,
}) => (
  <div className="relative h-12 w-[50%] sm:w-[80%] rounded-xl border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E]">
    <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full px-2">
      <input
        id={name}
        name={name}
        value={value}
        onChange={onChange}
        min="1"
        className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3"
        aria-label={label} // Add aria-label for accessibility
      />
      <div className="grid grid-rows-2 gap-1 relative">
        {' '}
        {/* Make this relative for absolute positioning */}
        <button
          type="button"
          onClick={() => onIncrement(name)}
          className="relative text-gray-400 transition-colors hover:text-gray-200"
          aria-label={`Increase ${label}`}
        >
          <span className="absolute top-[-10px] left-1/2 -translate-x-1/2 text-xs text-gray-500">
            {label}
          </span>
          <svg
            width="16"
            height="8"
            viewBox="0 0 16 8"
            fill="white"
            xmlns="http://www.w3.org/2000/svg"
            transform="rotate(-180)"
          >
            <path d="M8 8L0.205771 0H15.7942L8 8Z" fill="#8B939B" />
          </svg>
        </button>
        <button
          type="button"
          onClick={() => onDecrement(name)}
          className="relative text-gray-400 transition-colors hover:text-gray-200"
          aria-label={`Decrease ${label}`}
        >
          <span className="absolute bottom-[-10px] left-1/2 -translate-x-1/2 text-xs text-gray-500">
            {label}
          </span>
          <svg
            width="16"
            height="8"
            viewBox="0 0 16 8"
            fill="white"
            xmlns="http://www.w3.org/2000/svg"
            transform="rotate(180)"
          >
            <path d="M8 0L15.7942 8H0.205771L8 0Z" fill="#8B939B" />
          </svg>
        </button>
      </div>
    </div>
  </div>
);

export default NumberInput;
