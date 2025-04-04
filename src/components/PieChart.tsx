'use client';

import { Pie, PieChart, Sector } from 'recharts';
import type { PieSectorDataItem } from 'recharts/types/polar/Pie';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';
const chartData = [
  { browser: 'Process', visitors: 275, fill: 'var(--color-blueish)' },
  { browser: 'Wasted', visitors: 200, fill: 'var(--color-purplish)' },
  { browser: 'Setup', visitors: 187, fill: 'var(--color-greenish)' },
];

const chartConfig = {
  visitors: {
    label: 'Visitors',
  },
  chrome: {
    label: 'Chrome',
    color: 'hsl(var(--chart-1))',
  },
  safari: {
    label: 'Safari',
    color: 'hsl(var(--chart-2))',
  },
  firefox: {
    label: 'Firefox',
    color: 'hsl(var(--chart-3))',
  },
} satisfies ChartConfig;

export function PieChartTime() {
  return (
    <Card className="flex flex-col h-full w-full dark bg-[#10121E]">
      <CardHeader className="items-center py-1">
        <CardTitle className="text-xl p-0 m-0 text-center font-semibold text-zinc-400"  >
          Time Distribution
        </CardTitle>
      </CardHeader>
      <CardContent className="flex-1 m-0  flex items-center justify-center">
        <ChartContainer config={chartConfig} className="h-[150px] w-[130px]">
          <PieChart margin={{ top: 0, right: 5, bottom: 5, left: 5 }}>
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Pie
              data={chartData}
              dataKey="visitors"
              nameKey="browser"
              innerRadius={30}
              outerRadius={55}
              strokeWidth={4}
              activeIndex={0}
              activeShape={({
                outerRadius = 0,
                ...props
              }: PieSectorDataItem) => (
                <Sector {...props} outerRadius={outerRadius + 8} />
              )}
            />
          </PieChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
