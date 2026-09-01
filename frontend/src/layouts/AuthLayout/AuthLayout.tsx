import React from 'react';
import { Outlet } from 'react-router';

const AuthLayout: React.FC = () => {
  return (
    <div className="flex min-h-screen w-full flex-col justify-center items-center bg-bg px-5 md:px-20 py-5 md:py-10">
      <Outlet />
    </div>
  );
};

export default AuthLayout;
