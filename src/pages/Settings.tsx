import { useState } from 'react';

function Settings() {
  const [formData, setFormData] = useState({
    type: '',
    name: '',
    quantity: 1,
    workers: 1,
    load: 1,
    budget: 1,
    log: 1,
    height: 1,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === 'name' ? value : Math.max(1, Number(value) || 1),
    }));
  };

  const updateValue = (field: keyof typeof formData, change: number) => {
    setFormData((prev) => ({
      ...prev,
      [field]: Math.max(1, (prev[field] as number) + change),
    }));
  };
  const NumberInput = ({
    label,
    name,
  }: {
    label: string;
    name: keyof typeof formData;
  }) => (
    <div className="relative h-12 w-[50%] rounded-[8px] border border-gray-700">
      <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full px-2">
        <input
          id={name}
          name={name}
          value={formData[name]}
          onChange={handleChange}
          min="1"
          className="w-full bg-transparent font-bold text-2xl  text-center text-gray-400 focus:outline-none px-5 py-3"
          placeholder={label}
        />
        <div className="absolute grid grid-rows-2 gap-1 translate-x-[10%]">
          <button
            type="button"
            onClick={() => updateValue(name, 1)}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label={`Increase ${name}`}
          >
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
            onClick={() => updateValue(name, -1)}
            className="text-gray-400 transition-colors hover:text-gray-200"
            aria-label={`Decrease ${name}`}
          >
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

  return (
    <div className="flex justify-center text-xl sm:text-xs md:text-xs lg:text-xl ">
      <div className="bg-[#10121EE5] w-[50%] border-t mt-5 rounded-[8px]">
        <div className="grid grid-rows-2 gap-3">
          <div className="grid grid-rows-4 gap-5">
            <h1 className="font-bold text-3xl  sm:text-2xl md:text-2xl lg:text-3xl text-[#8B939B] flex justify-center items-center">
              Warehouse Properties
            </h1>

            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Maximum Load</span>
              <NumberInput label="Workers" name="workers" />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Initial Budget</span>
              <NumberInput label="Load" name="load" />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Number of Workers</span>
              <NumberInput label="Budget" name="budget" />
            </div>
          </div>

          <div className="grid grid-rows-3 gap-3">
            <h1 className="font-bold text-3xl text-[#8B939B] flex justify-center items-center">
              Warehouse Settings
            </h1>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Ray Tracing</span>
              <NumberInput label="Log" name="log" />
            </div>
            <div className="grid grid-cols-2 justify-items-start place-items-center mr-[20%] ml-[20%]">
              <span className="font-bold text-white">Maximum Log Days</span>
              <NumberInput label="" name="quantity" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
export default Settings;
