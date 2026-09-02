import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import LoginForm from '../../components/organisms/LoginForm/LoginForm';
import logo from '../../assets/logo/jobhub-logo.png';
import { useAuth } from '../../contexts/AuthContext';
import type { LoginPayload } from '../../types/auth.types';
import heroImage from '../../assets/images/landing_page/bro.svg';

const Login: React.FC = () => {
  const { login, isAuthenticated, role } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated && role) {
      if (role === 'admin') {
        navigate('/admin/dashboard', { replace: true });
      } else {
        navigate('/employee/dashboard', { replace: true });
      }
    }
  }, [isAuthenticated, role, navigate]);

  const handleLoginSubmit = async (payload: LoginPayload) => {
    setLoading(true);
    setError(null);
    try {
      const userRole = await login(payload);
      if (userRole === 'admin') {
        navigate('/admin/dashboard', { replace: true });
      } else {
        navigate('/employee/dashboard', { replace: true });
      }
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-h-screen flex flex-col md:flex-row items-center justify-center gap-6 md:gap-10 ">

      <div className="w-full md:w-3/5 p-25 hidden md:flex">
        <img
          src={heroImage}
          alt="Career Progress at JobHub"
          className="w-full h-auto object-contain transition-transform duration-500 hover:scale-105"
        />

      </div>

      <div className="w-full md:w-2/5 flex flex-col items-center justify-center gap-6">
        {/* Brand Header */}
        <div className="flex flex-col gap-2">
          <Link to="/" className="w-full flex items-center justify-center gap-2">
            <img src={logo} alt="JobHub Logo" className="w-10 md:w-20" />
            <h1 className="text-4xl md:text-6xl font-bold text-primary-hover">JobHub</h1>
          </Link>
          <p className="text-sm md:text-lg text-center font-medium text-text tracking-wide">
            One platform. Every opportunity. Your next move.
          </p>
        </div>


        {/* Login Form Organism */}
        <div className="w-full flex justify-center">
          <LoginForm onSubmit={handleLoginSubmit} loading={loading} error={error} />
        </div>
      </div>
    </div>
  );
};

export default Login;
