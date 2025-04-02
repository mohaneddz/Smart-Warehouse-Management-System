import { PieChartTime } from '@/components/PieChart';
import Card from '@/components/Card';
import Component from '@/components/Chart';
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
  ];

  return (
    <div>
      <main className="pt-40 flex flex-col items-center gap-4 w-full">
        {/* Top Cards Section */}
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 w-[90%] sm:w-[80%] md:w-[70%]">
          <Card
            mcolor="#35385E"
            up_down="5.12%"
            amount="79"
            title="Storage"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
          />
          <Card
            mcolor="#283C4A"
            up_down="5.12%"
            amount="79"
            title="Storage"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
          />
          <Card
            mcolor="#3F604D"
            up_down="5.12%"
            amount="79"
            title="Storage"
            src="/assets/icon/Storage.png"
            up_down_pic="/assets/icon/Good.png"
          />
        </div>

        <div className="grid grid-cols-[2fr_1fr] gap-4 w-[70%]">
          <div className="rounded-2xl p-4 flex flex-row gap-4 w-full">
            {/* Logs Section */}
            <div className="w-1/3 bg-[#10121E] rounded-2xl p-4">
              <h1 className="text-white text-2xl font-semibold text-center">
                Logs
              </h1>
              <ul className="p-2 space-y-4 text-white">
                {logs.map((log, index) => (
                  <li key={index} className="flex justify-between text-sm">
                    <span
                      className={`${log.type === '+' ? 'text-green-400' : 'text-red-400'} flex items-center`}
                    >
                      {log.type}{' '}
                      <span className="text-white px-2">
                        {log.amount} Items
                      </span>
                    </span>
                    <span className="text-gray-400">{log.time}</span>
                  </li>
                ))}
              </ul>
            </div>

            {/* Performance Chart Section */}
            <div className="flex-1 h-auto flex items-center justify-center rounded-2xl bg-[#10121E] p-4">
              <Component />
            </div>
          </div>

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
