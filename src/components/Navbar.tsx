'use client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const [active, setActive] = useState('home'); // Default active icon

  return (
    <div>
      <div className="w-full">
        <img src="/assets/picture/Headerimg.png" alt="" className="w-full" />
      </div>
      <div
      // set cols : 20% 30% 30% 20% 
        className="relative grid grid-cols-[20%_30%_0%_30%_20%] z-50 left-1/2 -translate-x-1/2 rounded-2xl 
        bg-[#0A0B14] w-[90%] max-w-[800px] h-min border border-[#30383E] -translate-y-1/2"
      >
        {/* 3D Layout */}
        <div
          onClick={() => {
            navigate('/warehouse-layout');
            setActive('layout');
          }}
          className={`flex justify-center items-center h-full rounded-l-2xl border-r border-[#30383E] hover:bg-[#13141F] cursor-pointer`}
        >
          <img
            className={`w-min h-min ${active === 'layout' ? 'opacity-100' : 'opacity-20'}`}
            src="/assets/svgs/World.svg"
            alt="Layout"
          />
        </div>

        {/* Stock Manager */}
        <div
          onClick={() => {
            navigate('/stock-manager');
            setActive('manager');
          }}
          className="flex justify-start pl-16 items-center h-full w-full border-r border-[#30383E] hover:bg-[#13141F] cursor-pointer "
        >
          <img
            className={`w-max h-min ${active === 'manager' ? 'opacity-100' : 'opacity-20'}`}
            src="/assets/svgs/Manage.svg"
            alt="Stock Manager"
          />
        </div>

        {/* Center Spacer */}
        <div className="flex justify-center items-center h-full">
          {/* This is just a spacer for the home button */}
        </div>

        {/* Logs */}
        <div
          onClick={() => {
            navigate('/logs');
            setActive('logs');
          }}
          className="flex justify-end pr-16 items-center h-full border-l border-[#30383E] hover:bg-[#13141F] cursor-pointer "
        >
          <img
            className={`w-max h-min ${active === 'logs' ? 'opacity-100' : 'opacity-20'}`}
            src="/assets/svgs/Logs.svg"
            alt="Logs"
          />
        </div>

        {/* Settings */}
        <div
          onClick={() => {
            navigate('/settings');
            setActive('settings');
          }}
          className="flex justify-center items-center h-full border-l border-[#30383E] rounded-r-2xl hover:bg-[#13141F] cursor-pointer"
        >
          <img
            className={`w-min h-min ${active === 'settings' ? 'opacity-100' : 'opacity-20'}`}
            src="/assets/svgs/Settings.svg"
            alt="Settings"
          />
        </div>

        {/* Home - Positioned absolutely in the center */}
        <div
          onClick={() => {
            navigate('/');
            setActive('home');
          }}
          className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 
          flex justify-center items-center rounded-full border border-[#30383E]
          w-24 h-24 max-w-24 max-h-24 bg-[#0A0B14] hover:bg-[#13141F] cursor-pointer"
        >
          <img
            src="/assets/svgs/Home.svg"
            alt="Home"
            className={`w-12 h-12 ${active === 'home' ? 'opacity-100' : 'opacity-20'}`}
          />
        </div>
      </div>
    </div>
  );
}

export default Navbar;