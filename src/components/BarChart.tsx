'use client';

import { Bar, BarChart, CartesianGrid, LabelList, XAxis } from 'recharts';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';

const chartData = [
  { category: 'Used Workers', workers: 186 },
  { category: 'Unused Workers', workers: 73 },
];

const chartConfig = {
  workers: {
    label: 'Workers',
    color: 'var(--color-greenish)',
  },
} satisfies ChartConfig;

export function BarChartRessources() {
  return (
    <Card className="bg-[#10121E] dark">
      <CardHeader>
        <CardTitle>Worker Allocation</CardTitle>
      </CardHeader>
      <CardContent>
        <ChartContainer config={chartConfig}>
          <BarChart
            accessibilityLayer
            data={chartData}
            margin={{
              top: 20,
            }}
          >
            <CartesianGrid vertical={false} />
            <XAxis
              dataKey="category"
              tickLine={false}
              tickMargin={10}
              axisLine={false}
            />
            <ChartTooltip
              cursor={false}
              content={<ChartTooltipContent hideLabel />}
            />
            <Bar dataKey="workers" fill="var(--color-workers)" radius={8}>
              <LabelList
                position="top"
                offset={12}
                className="fill-foreground"
                fontSize={12}
              />
            </Bar>
          </BarChart>
        </ChartContainer>
      </CardContent>
    </Card>
  );
}
