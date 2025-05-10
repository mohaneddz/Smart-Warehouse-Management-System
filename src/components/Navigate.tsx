'use client';

import { Card } from '@/components/ui/card';
import { useState } from 'react';

type CarouselSpacingProps = {
  onCardClick: (add: boolean, remove: boolean, manage: boolean) => void;
};

function CarouselSpacing({ onCardClick }: CarouselSpacingProps) {
  const [cards, setCards] = useState([
    { id: 1, label: 'Take from Inventory', position: 'left' },
    { id: 2, label: 'Add to Inventory', position: 'center' },
    { id: 3, label: 'Manage Inventory', position: 'right' },
  ]);

  const handleCardClick = (clickedCard: typeof cards[0]) => {
    if (clickedCard.position === 'center') return; // Already centered

    let Add = false;
    let Remove = false;
    let Manage = false;

    if (clickedCard.label === 'Add to Inventory') {
      Add = true;
    } else if (clickedCard.label === 'Take from Inventory') {
      Remove = true;
    } else {
      Manage = true;
    }

    onCardClick(Add, Remove, Manage);

    // Update positions
    setCards(cards.map(card => {
      if (card.id === clickedCard.id) {
        return { ...card, position: 'center' };
      } else if (card.position === 'center') {
        // Move currently centered card to where the clicked card was
        return { ...card, position: clickedCard.position };
      }
      return card;
    }));
  };

  const getCardStyles = (position: string) => {
    switch (position) {
      case 'left':
        return 'left-[15%] -translate-x-1/2 scale-90 opacity-70 hover:opacity-90';
      case 'center':
        return 'left-1/2 -translate-x-1/2 z-40 scale-110 bg-[#13101E] shadow-[0_0_20px_#6B86DE3B] opacity-100';
      case 'right':
        return 'left-[85%] -translate-x-1/2 scale-90 opacity-70 hover:opacity-90';
      default:
        return '';
    }
  };

  return (
    <div className="w-full md:w-[90%] lg:w-[70%] dark text-xl sm:text-[12px] md:text-xs lg:text-xl relative h-16 flex justify-center w-full mx-auto">
      {cards.map((card) => (
        <Card
          key={card.id}
          onClick={() => handleCardClick(card)}
          className={`
              absolute transition-all duration-500 ease-in-out cursor-pointer 
              w-max h-10 px-16 bg-[#2C2F3C] border-[#8B939B]
              flex justify-center items-center
              ${getCardStyles(card.position)}
            `}
        >
          {card.label}
        </Card>
      ))}
    </div>
  );
}

export default CarouselSpacing;