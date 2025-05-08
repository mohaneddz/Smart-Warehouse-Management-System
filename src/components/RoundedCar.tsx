'use client';

import * as React from 'react';
import type { CarouselApi } from '@/components/ui/carousel';
import { Card, CardContent } from '@/components/ui/card';
import {
  Carousel,
  CarouselContent,
  CarouselItem,
} from '@/components/ui/carousel';
import { Button } from '@/components/ui/button';

interface CarouselDemoProps {
  setSelectedImage: (image: string) => void;
}

export function CarouselDemo({ setSelectedImage }: CarouselDemoProps) {
  const [api, setApi] = React.useState<CarouselApi | null>(null);
  const [current, setCurrent] = React.useState(0);
  const [count, setCount] = React.useState(0);
  const [isAnimating, setIsAnimating] = React.useState(false);

  const images = [
    '/assets/picture/chemical.svg',
    '/assets/picture/electronic.svg',
    '/assets/picture/food.svg',
    '/assets/picture/material.svg',
    '/assets/picture/medicine.svg',
    '/assets/picture/household.svg',
  ];

  React.useEffect(() => {
    if (!api) return;

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap());
    setSelectedImage(images[api.selectedScrollSnap()]);

    api.on('select', () => {
      const index = api.selectedScrollSnap();
      setCurrent(index);
      setSelectedImage(images[index]);
    });
  }, [api, setSelectedImage, images]);

  const handlePrevious = React.useCallback(() => {
    if (isAnimating) return;
    setIsAnimating(true);
    
    if (current === 0) {
      // If at the first item, loop to the last item with animation
      api?.scrollTo(count - 1);
    } else {
      api?.scrollPrev();
    }
    
    setTimeout(() => setIsAnimating(false), 500); // Match with transition duration
  }, [api, current, count, isAnimating]);

  const handleNext = React.useCallback(() => {
    if (isAnimating) return;
    setIsAnimating(true);
    
    if (current === count - 1) {
      // If at the last item, loop to the first item with animation
      api?.scrollTo(0);
    } else {
      api?.scrollNext();
    }
    
    setTimeout(() => setIsAnimating(false), 500); // Match with transition duration
  }, [api, current, count, isAnimating]);

  return (
    <div className="relative">
      <Carousel 
        setApi={setApi} 
        className="w-[55%] max-w-xs"
        opts={{
          loop: true,
          align: "center",
        }}
      >
        <CarouselContent className="transition-all duration-300 ease-in-out">
          {images.map((imgSrc, index) => (
            <CarouselItem key={index} className="transition-all duration-300 ease-in-out">
              <div className="p-1">
                <Card 
                  className={`rounded-full bg-[#10121E] border-[#30383E] aspect-square overflow-hidden flex items-center justify-center transition-all duration-300 ease-in-out ${
                    current === index 
                      ? "scale-100 opacity-100 transform-gpu" 
                      : "scale-95 opacity-0 transform-gpu"
                  }`}
                >
                  <CardContent className="flex items-center justify-center">
                    <img
                      src={imgSrc}
                      alt={`Image ${index + 1}`}
                      className={`w-max h-max object-cover rounded-full cursor-pointer transition-all duration-300 ease-in-out transform-gpu ${
                        current === index ? "opacity-100 scale-100" : "opacity-0 scale-95"
                      }`}
                    />
                  </CardContent>
                </Card>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <div className="absolute left-[-40px] top-1/2 -translate-y-1/2 z-10">
          <Button
            variant="outline"
            size="icon"
            onClick={handlePrevious}
            className="h-8 w-8 rounded-full bg-transparent border-none transition-opacity duration-300 hover:opacity-80"
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="white"
              xmlns="http://www.w3.org/2000/svg"
              transform="rotate(-90)"
            >
              <path d="M8 0L15.7942 8H0.205771L8 0Z" fill="#8B939B" />
            </svg>
          </Button>
        </div>
        <div className="absolute right-[-40px] top-1/2 -translate-y-1/2 z-10">
          <Button
            variant="outline"
            size="icon"
            onClick={handleNext}
            className="h-8 w-8 rounded-full bg-transparent border-none transition-opacity duration-300 hover:opacity-80"
          >
            <svg
              width="16"
              height="8"
              viewBox="0 0 16 8"
              fill="white"
              xmlns="http://www.w3.org/2000/svg"
              transform="rotate(-90)"
            >
              <path d="M8 8L0.205771 0H15.7942L8 8Z" fill="#8B939B" />
            </svg>
          </Button>
        </div>
      </Carousel>
    </div>
  );
}