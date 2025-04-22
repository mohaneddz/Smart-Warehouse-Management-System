'use client';

import { Card } from '@/components/ui/card';
import { useState } from 'react';
type CarouselSpacingProps = {
  onCardClick: (add: boolean, remove: boolean, manage: boolean) => void;
};

function CarouselSpacing({ onCardClick }: CarouselSpacingProps) {
  const [cards, setCards] = useState([
    'Take from Inventory',
    'Add to Inventory',
    'Manage Inventory',
  ]);

  const handleCardClick = (index: number) => {
    let Add = false;
    let Remove = false;
    let Manage = false;

    if (cards[index] === 'Add to Inventory') {
      Add = true;
    } else if (cards[index] === 'Take from Inventory') {
      Remove = true;
    } else {
      Manage = true;
    }
    onCardClick(Add, Remove, Manage);
    if (index !== 1) {
      const newCards = [...cards];
      [newCards[1], newCards[index]] = [newCards[index], newCards[1]];
      setCards(newCards);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto dark text-xl sm:text-[12px] md:text-xs lg:text-xl">
      <div className="relative grid grid-cols-3 place-items-center gap-8 justify-items-center py-8">
        {cards.map((cardLabel, index) => (
          <Card
            key={cardLabel}
            onClick={() => handleCardClick(index)}
            className={`flex justify-center items-center border-[#8B939B]
              absolute transition-all duration-500 ease-in-out cursor-pointer w-[45%] h-10 bg-[#2C2F3C] 
              transform
              ${index === 0 ? 'left-0 -translate-x-1/2' : ''}
              ${index === 1 ? 'z-40 scale-120 bg-[#13101E] shadow-[0_0_20px_#6B86DE3B] border-[#8B939B] opacity-100' : 'z-10 scale-90 opacity-70 hover:opacity-90'}
              ${index === 2 ? 'right-0 translate-x-1/2' : ''}
            `}
          >
            {cardLabel}
          </Card>
        ))}
      </div>
    </div>
  );
}

export default CarouselSpacing;
