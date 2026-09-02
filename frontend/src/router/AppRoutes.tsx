import { Route, Routes } from 'react-router';
import PublicLayout from '../layouts/PublicLayout/PublicLayout';
import AuthLayout from '../layouts/AuthLayout/AuthLayout';
import AdminLayout from '../layouts/AdminLayout/AdminLayout';
import EmployeeLayout from '../layouts/EmployeeLayout/EmployeeLayout';
import ProtectedRoute from '../components/ProtectedRoute';
import LandingPage from '../pages/public/LandingPage';
import Login from '../pages/auth/Login';
import AdminDashboard from '../pages/admin/AdminDashboard';
import AdminJobRoles from '../pages/admin/AdminJobRoles';
import AdminJobPostings from '../pages/admin/AdminJobPostings';
import EmployeeDashboard from '../pages/employee/EmployeeDashboard';
import EmployeeJobOpportunities from '../pages/employee/EmployeeJobOpportunities';
import EmployeeMyApplications from '../pages/employee/EmployeeMyApplications';
import AdminJobApplications from '../pages/admin/AdminApplications';
import AdminJobApplication from '../pages/admin/AdminApplication';
import EmployeeProfile from '../pages/employee/EmployeeProfile';
import EmployeeJobDetails from '../pages/employee/EmployeeJobDetails';
import EmployeeApplicationTracking from '../pages/employee/EmployeeApplicationTracking';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<PublicLayout />}>
        <Route path="/" element={<LandingPage />} />
      </Route>

      <Route element={<AuthLayout />}>
        <Route path="/login" element={<Login />} />
      </Route>

      {/* TA / Admin Protected Routes */}
      <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
        <Route element={<AdminLayout />}>
          <Route path="/admin/dashboard" element={<AdminDashboard />} />
          <Route path="/admin/job-roles" element={<AdminJobRoles />} />
          <Route path="/admin/job-postings" element={<AdminJobPostings />} />
          <Route path="/admin/job-applications" element={<AdminJobApplications />} />
          <Route path="/admin/job-applications/:id" element={<AdminJobApplication />} />
        </Route>
      </Route>

      {/* Employee Protected Routes */}
      <Route element={<ProtectedRoute allowedRoles={['user']} />}>
        <Route element={<EmployeeLayout />}>
          <Route path="/employee/dashboard" element={<EmployeeDashboard />} />
          <Route path="/employee/job-opportunities" element={<EmployeeJobOpportunities />} />
          <Route path="/employee/my-applications" element={<EmployeeMyApplications />} />
          <Route path="/employee/profile" element={<EmployeeProfile />} />
          <Route path="/employee/job-details/:id" element={<EmployeeJobDetails />} />
          <Route path="/employee/applications/:id" element={<EmployeeApplicationTracking />} />
        </Route>
      </Route>
    </Routes>
  );
};

export default AppRoutes;
