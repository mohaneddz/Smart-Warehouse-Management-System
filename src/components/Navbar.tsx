'use client';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();

  return (
    <div>
      <table className="relative top-25 left-1/2 -translate-x-1/2 rounded-2xl bg-[#0A0B14] w-[590px] h-[77.97px]">
        <tbody>
          <tr>
            <td className="w-[118px]">
              <div
                onClick={() => navigate('/warehouse-layout')}
                className="flex justify-center w-full h-full items-center rounded-l-2xl border border-[#30383E] hover:bg-[#13141F] cursor-pointer"
              >
                <img
                  className="w-[64px] h-[50px]"
                  src="/assets/icon/America.png"
                  alt="America"
                />
              </div>
            </td>
            <td className="w-[118px]">
              <div
                onClick={() => navigate('/stock-manager')}
                className="flex justify-center items-center w-full h-full border-r-0 border border-[#30383E] hover:bg-[#13141F] cursor-pointer"
              >
                <img
                  className="w-[54px] h-[54px]"
                  src="/assets/icon/Tesseract.png"
                  alt="Tesseract"
                />
              </div>
            </td>
            <td className="w-[118px] relative border-r-0 border-l-0 border border-[#30383E]">
              <div
                onClick={() => navigate('/')}
                className="flex justify-center items-center absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 rounded-full border border-[#30383E] w-[123px] h-[123px] bg-[#0A0B14] hover:bg-[#13141F] cursor-pointer"
              >
                <img
                  className="w-[73px] h-[63px]"
                  src="/assets/icon/Vector.png"
                  alt="Vector"
                />
              </div>
            </td>
            <td className="w-[118px]">
              <div
                onClick={() => navigate('/logs')}
                className="flex justify-center items-center w-full h-full border-l-0 border border-[#30383E] hover:bg-[#13141F] cursor-pointer"
              >
                <img
                  className="w-[52px] h-[64px]"
                  src="/assets/icon/Scroll.png"
                  alt="Scroll"
                />
              </div>
            </td>
            <td className="w-[118px]">
              <div
                onClick={() => navigate('/settings')}
                className="flex justify-center items-center rounded-r-2xl w-full h-full border-l-0 border border-[#30383E] hover:bg-[#13141F] cursor-pointer"
              >
                <img
                  className="w-[41px] h-[44px]"
                  src="/assets/icon/settings.png"
                  alt="Settings"
                />
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Navbar;
