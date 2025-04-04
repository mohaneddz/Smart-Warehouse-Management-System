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
    color: 'var(--color-purplish)',
  },
  Efficiency: {
    label: 'Efficiency',
    color: 'var(--color-blueish)',
  },
  Revenue: {
    label: 'Revenue',
    color: 'var(--color-greenish)',
  },
} satisfies ChartConfig;

function Chart() {
  return (
    <div className="dark w-full h-full">
      <Card className="bg-[#10121E] text-foreground ">
        <CardHeader>
          <CardTitle className="place-items-center text-2xl">
            Warehouse Performance
          </CardTitle>
        </CardHeader >
        <CardContent>
          <ChartContainer config={chartConfig} className="h-70 -ml-4 mr-4">
            <AreaChart
              accessibilityLayer
              data={chartData}
              margin={{
                left: 0,
                right: 0,
                top: 0,
                bottom: 0,
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
          <div className="flex w-full justify-around">
            <div className="flex items-center gap-2">
              <img src="/assets/svgs/BlueIndex.svg" alt="Chart" className="w-10 h-10" />
              <p className='text-zinc-400 text-sm'>Storage</p>
            </div>
            <div className="flex items-center gap-2">
              <img src="/assets/svgs/PurpleIndex.svg" alt="Chart" className="w-10 h-10" />
              <p className='text-zinc-400 text-sm'>Efficiency</p>
            </div>
            <div className="flex items-center gap-2">
              <img src="/assets/svgs/GreenIndex.svg" alt="Chart" className="w-10 h-10" />
              <p className='text-zinc-400 text-sm'>Revenue</p>
            </div>
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
export default Chart;
