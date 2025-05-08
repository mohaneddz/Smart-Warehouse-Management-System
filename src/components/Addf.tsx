import React, { useState } from 'react';
import { CarouselDemo as Carousel } from '../components/RoundedCar.tsx';
import { NumberInput } from '@/components/ui/number-input';

const Form = () => {
  const [selectedImage, setSelectedImage] = useState<string>('');
  const [formData, setFormData] = useState({
    type: '',
    name: '',
    quantity: 0,
    weight: 0,
    expiry: 0,
    fragility: 0,
    width: 0,
    height: 0,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form data submitted:', formData);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex flex-col justify-items-center place-items-center gap-24 mb-24"
    >
      <div className="flex justify-center items-center translate-x-18 font-[Arsenal]">
        <Carousel setSelectedImage={setSelectedImage} />
        <input type="hidden" name="selectedImage" value={selectedImage} />
      </div>

      <div
        className="relative rounded-xl h-12 w-[80%] border border-gray-700
         bg-gradient-to-r from-[#10121E] via-[#7F8387]/50 to-[#10121E]"
      >
        <div className="flex items-center justify-center h-full bg-[#10121E] opacity-80 rounded-xl ">
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

      <div
        className="w-[80%] grid grid-cols-2 gap-4 justify-items-center place-items-center
         sm:grid-cols-1 md:grid-cols-1 lg:grid-cols-2"
      >
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Weight</span>
          <NumberInput
            value={formData.weight}
            onChange={(value) => setFormData(prev => ({ ...prev, weight: value }))}
            label="Weight"
            showLabel={true}
            className="w-full"
            integersOnly={false}
          />
        </div>
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Height</span>
          <NumberInput
            value={formData.height}
            onChange={(value) => setFormData(prev => ({ ...prev, height: value }))}
            label="Height"
            showLabel={true}
            className="w-full"
            integersOnly={false}
          />
        </div>
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Width</span>
          <NumberInput
            value={formData.width}
            onChange={(value) => setFormData(prev => ({ ...prev, width: value }))}
            label="Width"
            showLabel={true}
            className="w-full"
            integersOnly={true}
          />
        </div>
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Expiry</span>
          <NumberInput
            value={formData.expiry}
            onChange={(value) => setFormData(prev => ({ ...prev, expiry: value }))}
            label="Expiry"
            showLabel={true}
            className="w-full"
            integersOnly={true}
          />
        </div>
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Fragility</span>
          <NumberInput
            value={formData.fragility}
            onChange={(value) => setFormData(prev => ({ ...prev, fragility: value }))}
            label="Fragility"
            showLabel={true}
            className="w-full"
            integersOnly={true}
          />
        </div>
        <div className="flex flex-col gap-2 w-full">
          <span className="text-gray-400">Quantity</span>
          <NumberInput
            value={formData.quantity}
            onChange={(value) => setFormData(prev => ({ ...prev, quantity: value }))}
            label="Quantity"
            showLabel={true}
            className="w-full"
            integersOnly={true}
          />
        </div>
      </div>

      <div className="flex justify-center ">
        <button
          type="submit"
          className="transition-all duration-300 ease-in-out cursor-pointer w-50 h-10 bg-[#2C2F3C] rounded-xl hover:scale-110 hover:shadow-lg hover:bg-[#43386a] 
          hover:shadow-purplish/50 hover:border-blue-400 hover:opacity-100 text-center text-gray-400 focus:outline-none px-5 py-3 flex justify-center items-center"
        >
          Add
        </button>
      </div>
    </form>
  );
};

export default Form;
