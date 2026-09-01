import { Outlet } from 'react-router';

const EmployeeLayout = () => {
  return (
    <div className="min-h-screen w-full bg-bg flex flex-col">
      <main className="flex-1 w-full p-6">
        <Outlet />
      </main>
    </div>
  );
};

export default EmployeeLayout;
