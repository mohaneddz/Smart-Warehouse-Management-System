import React, { useState } from 'react';
import { CarouselDemo as Carousel } from '../components/RoundedCar.tsx';

const Form = () => {
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [formData, setFormData] = useState({
    type: '',
    name: '',
    quantity: 1,
    weight: 1,
    expiry: 1,
    fragility: 1,
    width: 1,
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form data submitted:', formData);
  };

  const NumberInput = ({
    label,
    name,
  }: {
    label: string;
    name: keyof typeof formData;
  }) => (
    <div className="relative h-12 w-72 rounded-xl border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E]">
      <div className="flex items-center justify-between bg-[#10121E] opacity-80 rounded-xl w-full h-full px-2">
        <input
          id={name}
          name={name}
          value={formData[name]}
          onChange={handleChange}
          min="1"
          className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3"
          placeholder={label}
        />
        <div className="grid grid-rows-2 gap-1 ">
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
    <form onSubmit={handleSubmit} className="space-y-4 p-4">
      <div className="flex justify-center items-center translate-x-18">
        <Carousel setSelectedImage={setSelectedImage} />
        <input type="hidden" name="selectedImage" value={selectedImage} />
      </div>

      <div className="grid grid-rows-2 justify-items-center gap-0 place-items-center">
        <div className="relative rounded-xl h-12 w-72 border border-gray-700 bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E]">
          <div className="flex items-center h-full justify-between bg-[#10121E] opacity-80 rounded-xl w-full">
            <input
              type="text"
              id="name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="w-full bg-transparent text-center text-gray-400 focus:outline-none px-5 py-3"
              placeholder="Name"
            />
          </div>
        </div>

        <div className="grid grid-cols-2 gap-2 justify-items-center place-items-center">
          <NumberInput label="Quantity" name="quantity" />
          <NumberInput label="Weight" name="weight" />
          <NumberInput label="Height" name="height" />
          <NumberInput label="Width" name="width" />
          <NumberInput label="Expiry" name="expiry" />
          <NumberInput label="Fragility" name="fragility" />
        </div>
      </div>

      <div className="flex justify-center mt-4">
        <button
          type="submit"
          className="transition-all duration-300 ease-in-out cursor-pointer w-50 h-10 bg-[#2C2F3C] rounded-xl hover:scale-110 hover:shadow-lg hover:bg-[#13101E] 
          hover:shadow-blue-500/50 hover:border-blue-400 hover:opacity-100 text-center text-gray-400 focus:outline-none px-5 py-3"
        >
          Add
        </button>
      </div>
    </form>
  );
};

export default Form;
