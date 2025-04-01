import Card from '../components/Card.tsx';
import Navbar from '../components/Navbar.tsx';

const Home = () => {
  return (
    <div>
      <Navbar />
      {/* body section */}
      <main className="pt-40 flex flex-col items-center gap-4 w-full">
        {/* Cards Section */}
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

        {/* Bottom Section */}
        <div className="grid grid-cols-3 gap-4 w-[90%] sm:w-[80%] md:w-[70%] h-[80%]">
          {/* Left Section (LOGS) */}
          <div className="col-span-1 rounded-2xl bg-[#10121E] p-4 ">
            <h1 className="text-white text-lg font-semibold">LOGS</h1>
            <ul className="p-2 space-y-2 text-white">
              <li>
                <p>
                  <span>+</span>20 items <span>today</span>
                </p>
              </li>
              <li>
                <p>
                  <span>+</span>20 items <span>today</span>
                </p>
              </li>
              <li>
                <p>
                  <span>+</span>20 items <span>today</span>
                </p>
              </li>
              <li>
                <p>
                  <span>+</span>20 items <span>today</span>
                </p>
              </li>
            </ul>
          </div>

          {/* Right Section */}
          <div className="col-span-2 bg-[#151720] p-4 rounded-2xl"></div>

          {/* Bottom Grid */}
          {/* <div className="col-span-3 grid grid-rows-2 gap-2">
            <div className="bg-[#1A1C28] p-4 rounded-xl"></div>
            <div className="bg-[#202230] p-4 rounded-xl"></div>
          </div> */}
        </div>
      </main>
    </div>
  );
};
export default Home;
