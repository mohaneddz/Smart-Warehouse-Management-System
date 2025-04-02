'use client';

import { TrendingUp } from 'lucide-react';
import { Area, AreaChart, CartesianGrid, XAxis, YAxis } from 'recharts';

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from '@/components/ui/card';
import {
  type ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart';

const chartData = [
  { month: 'January', Storage: 20, Efficiency: 40, Revenue: 60 },
  { month: 'February', Storage: 45, Efficiency: 65, Revenue: 80 },
  { month: 'March', Storage: 30, Efficiency: 50, Revenue: 70 },
];

const chartConfig = {
  Storage: {
    label: 'Storage',
    color: 'hsl(var(--chart-1))',
  },
  Efficiency: {
    label: 'Efficiency',
    color: 'hsl(var(--chart-2))',
  },
  Revenue: {
    label: 'Revenue',
    color: 'hsl(var(--chart-3))',
  },
} satisfies ChartConfig;

function Component() {
  return (
    <div className="dark w-full h-full">
      <Card className="bg-[#10121E] text-foreground ">
        <CardHeader>
          <CardTitle className="place-items-center">
            Warehouse Performance
          </CardTitle>
          <CardDescription className="text-muted-foreground">
            Description
          </CardDescription>
        </CardHeader>
        <CardContent>
          <ChartContainer config={chartConfig}>
            <AreaChart
              accessibilityLayer
              data={chartData}
              margin={{
                left: 20,
                right: 20,
                top: 20,
                bottom: 20,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="month"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value.slice(0, 3)}
              />
              <YAxis tickLine={false} axisLine={false} tickMargin={8} />
              <ChartTooltip
                cursor={false}
                content={<ChartTooltipContent indicator="dot" />}
              />
              <Area
                dataKey="Storage"
                type="natural"
                fill="var(--color-Storage)"
                fillOpacity={0.4}
                stroke="var(--color-Storage)"
                stackId="a"
              />
              <Area
                dataKey="Efficiency"
                type="natural"
                fill="var(--color-Efficiency)"
                fillOpacity={0.4}
                stroke="var(--color-Efficiency)"
                stackId="a"
              />
              <Area
                dataKey="Revenue"
                type="natural"
                fill="var(--color-Revenue)"
                fillOpacity={0.4}
                stroke="var(--color-Revenue)"
                stackId="a"
              />
            </AreaChart>
          </ChartContainer>
        </CardContent>
        <CardFooter>
          <div className="flex w-full items-start gap-2 text-sm">
            <div className="grid gap-2">
              <div className="flex items-center gap-2 font-medium leading-none">
                {' '}
                <TrendingUp className="h-4 w-4" />
              </div>
              <div className="flex items-center gap-2 leading-none text-muted-foreground"></div>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
export default Component;
