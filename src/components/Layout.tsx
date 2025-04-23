import React from 'react';
import { Outlet } from 'react-router-dom';
import Header from './Header'; // Your header component

function Layout() {
  return (
    <div>
      <Header />
      <div className="content">
        <Outlet />
      </div>
      {/* Optional: Footer */}
    </div>
  );
}

export default Layout;
