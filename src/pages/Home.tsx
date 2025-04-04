import { PieChartTime } from '@/components/PieChart';
import Card from '@/components/Card';
import Chart from '@/components/Chart';
import { BarChartRessources } from '@/components/BarChart';

const Home = () => {
  const logs = [
    { type: '+', amount: 10, time: 'today' },
    { type: '-', amount: 20, time: 'yesterday' },
    { type: '-', amount: 5, time: '2d ago' },
    { type: '+', amount: 10, time: '2d ago' },
    { type: '+', amount: 15, time: '4d ago' },
    { type: '+', amount: 40, time: 'week ago' },
    { type: '-', amount: 50, time: '2 weeks ago' },
    { type: '+', amount: 25, time: '2 weeks ago' },
    { type: '+', amount: 35, time: 'month ago' },
    { type: '-', amount: 20, time: 'month ago' },
    { type: '+', amount: 50, time: '2 months ago' },
    { type: '-', amount: 30, time: '2 months ago' },
    { type: '+', amount: 20, time: '3 months ago' },
    { type: '+', amount: 15, time: '4 months ago' },
    { type: '-', amount: 20, time: '5 months ago' },
  ];

  return (
    <div>
      <main className="pt-40 flex flex-col items-center gap-4 w-full">

        {/* Top Cards Section */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8 w-[90%] sm:w-[80%] md:w-[70%] justify-items-center">
          <Card
            mcolor="bg-purplish"
            up_down="5.12"
            amount="79"
            title="Storage"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
            className='justify-self-start'
            up={true}
          />
          <Card
            mcolor="bg-blueish"
            up_down="5.12"
            amount="79"
            title="Efficiency"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
            className='justify-self-center'
            up={false}
          />
          <Card
            mcolor="bg-greenish"
            up_down="5.12"
            amount="79"
            title="Revenue"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
            className='justify-self-end'
            up={true}
          />
        </div>

        <img src="/assets/svgs/Seperator.svg" alt="Chart" className="w-full h-10" />

        <div className="grid grid-cols-[2fr_1fr] gap-4 w-[90%] sm:w-[80%] md:w-[70%]">

          <div className="rounded-2xl flex flex-row gap-4 w-full">

            {/* Left Section */}
            <div className="w-1/3 bg-[#10121E] rounded-2xl h-full overflow-hidden relative p-4">
              <div className="border-1 border-border rounded-2xl p-2 h-full">
                <h1 className="text-center font-semibold text-zinc-400 text-2xl">
                  Logs
                </h1>
                <ul className="p-2 space-y-4 text-white">
                  {logs.map((log, index) => (
                    <li key={index} className="flex justify-between text-sm">
                      <span
                        className={`${log.type === '+' ? 'text-green-400' : 'text-red-400'} flex items-center`}
                      >
                        {log.type}{' '}
                        <span className="text-slate-300 truncate px-2">
                          {log.amount} Items
                        </span>
                      </span>
                      <span className="text-gray-400 truncate">{log.time}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Middle Section */}
            <div className="flex-1 h-auto flex items-center justify-center rounded-2xl bg-[#10121E] p-4">
              <Chart />
            </div>
          </div>

          {/* Right Section */}
          <div className="grid grid-rows-2 gap-4">
            <div className="rounded-2xl bg-[#10121E] p-4">
              <PieChartTime />
            </div>
            <div className="rounded-2xl bg-[#10121E] p-4">
              <BarChartRessources />
            </div>
          </div>
        </div>
      </main>
    </div>
  );
};

export default Home;
