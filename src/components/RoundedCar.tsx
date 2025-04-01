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

export function CarouselDemo() {
  const [api, setApi] = React.useState<CarouselApi>();
  const [current, setCurrent] = React.useState(0);
  const [count, setCount] = React.useState(0);

  React.useEffect(() => {
    if (!api) {
      return;
    }

    setCount(api.scrollSnapList().length);
    setCurrent(api.selectedScrollSnap() + 1);

    api.on('select', () => {
      setCurrent(api.selectedScrollSnap() + 1);
    });
  }, [api]);

  const scrollPrev = React.useCallback(() => {
    api?.scrollPrev();
  }, [api]);

  const scrollNext = React.useCallback(() => {
    api?.scrollNext();
  }, [api]);

  return (
    <div className="relative">
      <Carousel setApi={setApi} className="w-[55%] max-w-xs ">
        <CarouselContent>
          {Array.from({ length: 5 }).map((_, index) => (
            <CarouselItem key={index}>
              <div className="p-1">
                <Card className="rounded-full bg-[#10121E] border-[#30383E] aspect-square">
                  <CardContent className="flex items-center justify-center p-6">
                    <img
                      src={`https://example.com/image-${index + 1}.jpg`} // Replace with your image URL
                      alt={`Image ${index + 1}`}
                      className="w-full h-auto rounded-lg cursor-pointer"
                    />
                  </CardContent>
                </Card>
              </div>
            </CarouselItem>
          ))}
        </CarouselContent>
        <div className="absolute left-[-40px] top-1/2 -translate-y-1/2 z-10 ">
          <Button
            variant="outline"
            size="icon"
            onClick={scrollPrev}
            className="h-8 w-8 rounded-full bg-transparent border-none"
            disabled={current === 1}
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
            </svg>{' '}
          </Button>
        </div>
        <div className="absolute right-[-40px] top-1/2 -translate-y-1/2 z-10">
          <Button
            variant="outline"
            size="icon"
            onClick={scrollNext}
            className="h-8 w-8 rounded-full  bg-transparent border-none"
            disabled={current === count}
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
