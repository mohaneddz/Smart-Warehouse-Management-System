import React, { useState } from 'react';
import Input from '../components/Input.tsx';
import Name from '../components/Name.tsx';

import { Button } from '@/components/ui/button';

function Addform() {
  // State to store form data
  const [formData, setFormData] = useState({
    name: '',
    quantity: 1,
    weight: 1,
    expiry: '',
    fragility: '',
    width: 1,
    height: 1,
  });

  // Handle input change
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  // Handle number inputs (quantity, weight, etc.)
  const handleNumberChange = (name: string, value: number) => {
    setFormData((prevState) => ({
      ...prevState,
      [name]: value,
    }));
  };

  // Handle form submission
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log('Form submitted with data:', formData);
    // You can process formData here, e.g., send it to an API or perform validation
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="grid grid-rows-2 justify-items-center gap-2 place-items-center"
    >
      <div className="grid grid-rows-5 gap-2 justify-items-center place-items-center mt-0">
        <div className="w-[50%]">
          <Name
            defaultValue={formData.name}
            onChange={(value) =>
              handleChange({ target: { name: 'name', value } })
            }
          />
        </div>

        <div className="grid grid-cols-2 gap-2 justify-items-center place-items-center">
          <Input
            text="Quantity"
            name="quantity"
            value={formData.quantity}
            onChange={(value: number) => handleNumberChange('quantity', value)}
          />
          <Input
            text="Weight"
            name="weight"
            value={formData.weight}
            onChange={(value: number) => handleNumberChange('weight', value)}
          />
        </div>
        <div className="grid grid-cols-2 gap-2 justify-items-center">
          <Input
            text="Expiry"
            name="expiry"
            value={formData.expiry}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleChange(e)
            }
          />
          <Input
            text="Fragility"
            name="fragility"
            value={formData.fragility}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              handleChange(e)
            }
          />
        </div>
        <div className="grid grid-cols-2 gap-2 justify-items-center">
          <Input
            text="Width"
            name="width"
            value={formData.width}
            onChange={(value: number) => handleNumberChange('width', value)}
          />
          <Input
            text="Height"
            name="height"
            value={formData.height}
            onChange={(value: number) => handleNumberChange('height', value)}
          />
        </div>
        <div className="w-[50%]">
          <Button
            variant="outline"
            className="bg-[#10121E] text-sm font-medium uppercase text-gray-400 rounded-xl border border-gray-700"
            type="submit"
          >
            ADD
          </Button>
        </div>
      </div>
    </form>
  );
}

export default Addform;
