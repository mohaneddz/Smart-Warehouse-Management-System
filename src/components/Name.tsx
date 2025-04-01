'use client';

import { cn } from '@/lib/utils';

interface QuantityInputProps {
  defaultValue?: number;
  min?: number;
  max?: number;
  step?: number;
  onChange?: (value: number) => void;
  className?: string;
}

function Name({ className }: QuantityInputProps) {
  return (
    <div
      className={cn(
        'relative flex items-center justify-between rounded-xl border border-gray-700 bg-gray-900 shadow-sm px-5 py-3 w-[50%] h-13',
        className,
      )}
    >
      <div className="flex-1 text-center">
        <span className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3">
          Name
        </span>
      </div>
    </div>
  );
}
export default Name;
