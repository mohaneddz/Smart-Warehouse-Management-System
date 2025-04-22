'use client';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function Navbar() {
  const navigate = useNavigate();
  const [active, setActive] = useState('home'); // Default active icon

  return (
    <div
      className="relative top-25 grid grid-cols-5  sm:[grid-template-columns:1fr_1fr_1.6fr_1fr_1fr] lg:grid-cols-5 md:grid-cols-5
 left-1/2 -translate-x-1/2 rounded-2xl bg-[#0A0B14] w-[40%] h-max border border-[#30383E]"
    >
      {/* 3D Layout */}
      <div
        onClick={() => {
          navigate('/warehouse-layout');
          setActive('layout');
        }}
        className={`flex justify-center items-center h-full rounded-l-2xl border-r border-[#30383E] hover:bg-[#13141F] cursor-pointer p-2 sm:p-3`}
      >
        <img
          className={`w-[60%] h-[60%] sm:w-[70%] sm:h-[70%] ${active === 'layout' ? 'opacity-100' : 'opacity-20'}`}
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
        className="flex justify-center  overflow-x-hidden items-center h-full w-full  hover:bg-[#13141F] cursor-pointer "
      >
        <img
          className={`w-[70%] h-[70%] ${active === 'manager' ? 'opacity-100' : 'opacity-20'}`}
          src="/assets/svgs/Manage.svg"
          alt="Stock Manager"
        />
      </div>

      <div
        className={`${active === 'home' ? 'opacity-100' : 'opacity-20'}`}
      ></div>

      {/* Home */}
      <div
        onClick={() => {
          navigate('/');
          setActive('home');
        }}
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 z-50 flex justify-center items-center rounded-full border border-[#30383E]
          min-w-16 min-h-16 w-[8vw] h-[8vw] sm:w-[6rem] sm:h-[6rem] md:w-16 md:h-16 lg:w-[8rem] lg:h-[8rem]
           bg-[#0A0B14] hover:bg-[#13141F] cursor-pointer"
      >
        <img
          src="/assets/svgs/Home.svg"
          alt="Home"
          className={`${active === 'home' ? 'opacity-100' : 'opacity-20'} w-[70%] h-[70%]`}
        />
      </div>

      {/* Logs */}
      <div
        onClick={() => {
          navigate('/logs');
          setActive('logs');
        }}
        className="flex justify-center items-center h-full border-r border-[#30383E] hover:bg-[#13141F] cursor-pointer"
      >
        <img
          className={`w-[50%] h-[80%] ${active === 'logs' ? 'opacity-100' : 'opacity-20'}`}
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
        className="flex justify-center items-center h-full rounded-r-2xl hover:bg-[#13141F] cursor-pointer"
      >
        <img
          className={`w-[50%] h-[50%] ${active === 'settings' ? 'opacity-100' : 'opacity-20'}`}
          src="/assets/svgs/Settings.svg"
          alt="Settings"
        />
      </div>
    </div>
  );
}

export default Navbar;
