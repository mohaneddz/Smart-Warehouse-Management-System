import { useState } from 'react';
import { NumberInput } from '@/components/ui/number-input';
import { BooleanInput } from '@/components/ui/boolean-input';

interface FormData {
  workers: number;
  load: number;
  budget: number;
  rayTracing: boolean;
  maxLogDays: number;
}

function Settings() {
  const [formData, setFormData] = useState<FormData>({
    workers: 0,
    load: 0,
    budget: 0,
    rayTracing: false,
    maxLogDays: 0,
  });

  return (
    <div className="flex justify-center text-xl sm:text-xs md:text-xs lg:text-xl">
      <div className="bg-[#10121EE5] min-w-[90%] border-t mt-5 rounded-[8px]">
        <div className="p-8">
          <h1 className="font-bold text-3xl sm:text-2xl md:text-2xl lg:text-3xl text-[#8B939B] flex justify-center items-center mb-8">
            Warehouse Items
          </h1>

          <div className="grid grid-rows-3 gap-3">
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Maximum Load</span>
              <NumberInput
                value={formData.load}
                onChange={(value) => setFormData(prev => ({ ...prev, load: value }))}
                label="Load"
                min={0}
                showLabel={true}
                className="w-[200px]"
              />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Initial Budget</span>
              <NumberInput
                value={formData.budget}
                onChange={(value) => setFormData(prev => ({ ...prev, budget: value }))}
                label="Budget"
                min={0}
                showLabel={true}
                className="w-[200px]"
              />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Number of Workers</span>
              <NumberInput
                value={formData.workers}
                onChange={(value) => setFormData(prev => ({ ...prev, workers: value }))}
                label="Workers"
                min={0}
                showLabel={true}
                className="w-[200px]"
              />
            </div>
          </div>

          <div className="grid grid-rows-3 gap-3 mt-8">
            <h1 className="font-bold text-3xl text-[#8B939B] flex justify-center items-center">
              Warehouse Settings
            </h1>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Maximum Log Days</span>
              <NumberInput
                value={formData.maxLogDays}
                onChange={(value) => setFormData(prev => ({ ...prev, maxLogDays: value }))}
                label="Days"
                min={0}
                max={365}
                showLabel={true}
                className="w-[200px]"
              />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Ray Tracing</span>
              <BooleanInput
                value={formData.rayTracing}
                onChange={(value) => setFormData(prev => ({ ...prev, rayTracing: value }))}
                label="Enable"
                className="self-center w-full"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Settings;
