'use client';

import { Card } from '@/components/ui/card';
import { useState } from 'react';

function CarouselSpacing() {
  // Initialise les cartes avec trois éléments
  const [cards, setCards] = useState([
    'Take from Inventory',
    'Add to Inventory',
    'Manage Inventory',
  ]);

  // Fonction pour échanger une carte latérale avec la carte du centre
  const handleCardClick = (index: number) => {
    if (index !== 1) {
      const newCards = [...cards];
      [newCards[1], newCards[index]] = [newCards[index], newCards[1]];
      setCards(newCards);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto  dark ">
      <div className="relative flex items-center gap-8 justify-center py-8">
        {cards.map((cardNumber, index) => (
          <Card
            key={cardNumber}
            onClick={() => handleCardClick(index)}
            className={`flex justify-center items-center
              absolute transition-all duration-300 ease-in-out cursor-pointer w-50 h-10  bg-[#2C2F3C]
              ${index === 0 ? 'left-0 -translate-x-1/2' : ''}
              ${index === 1 ? 'z-40 scale-120 shadow-lg bg-[#13101E] shadow-blue-500/50 border-blue-400 opacity-100' : 'z-10 scale-90 opacity-70 hover:opacity-90'}
              ${index === 2 ? 'right-0 translate-x-1/2' : ''}
            `}
          >
            {cardNumber}
          </Card>
        ))}
      </div>
    </div>
  );
}

export default CarouselSpacing;
