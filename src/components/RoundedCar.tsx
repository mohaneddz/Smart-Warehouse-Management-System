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

  const images = [
    '/assets/picture/axe.png',
    '/assets/picture/box.png',
    '/assets/picture/cable.png',
    '/assets/picture/shirt.png',
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
  }, [api, setSelectedImage]);

  return (
    <div className="relative">
      <Carousel setApi={setApi} className="w-[55%] max-w-xs">
        <CarouselContent>
          {images.map((imgSrc, index) => (
            <CarouselItem key={index}>
              <div className="p-1">
                <Card className="rounded-full bg-[#10121E] border-[#30383E] aspect-square overflow-hidden flex items-center justify-center">
                  <CardContent className="flex items-center justify-center p-6">
                    <img
                      src={imgSrc}
                      alt={`Image ${index + 1}`}
                      className="w-full h-full object-cover rounded-full cursor-pointer"
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
            onClick={() => api?.scrollPrev()}
            className="h-8 w-8 rounded-full bg-transparent border-none"
            disabled={!api?.canScrollPrev()}
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
            onClick={() => api?.scrollNext()}
            className="h-8 w-8 rounded-full bg-transparent border-none"
            disabled={!api?.canScrollNext()}
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
