import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router';
import LoginForm from '../../components/organisms/LoginForm/LoginForm';
import Logo from '../../components/atoms/Logo/Logo';
import { useAuth } from '../../contexts/AuthContext';
import type { LoginPayload } from '../../types/auth.types';
import heroImage from '../../assets/images/landing_page/Career-progress-amico.svg';

const Login: React.FC = () => {
  const { login, isAuthenticated, role } = useAuth();
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Auto redirect if already authenticated
  React.useEffect(() => {
    if (isAuthenticated && role) {
      if (role === 'admin') {
        navigate('/admin', { replace: true });
      } else {
        navigate('/employee', { replace: true });
      }
    }
  }, [isAuthenticated, role, navigate]);

  const handleLoginSubmit = async (payload: LoginPayload) => {
    setLoading(true);
    setError(null);
    try {
      const userRole = await login(payload);
      if (userRole === 'admin') {
        navigate('/admin', { replace: true });
      } else {
        navigate('/employee', { replace: true });
      }
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check your credentials.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-6xl flex flex-col md:flex-row items-center justify-between gap-10 md:gap-16 my-auto">
      {/* Left side: Vector Illustration */}
      <div className="w-full md:w-1/2 flex flex-col items-center justify-center p-4 md:p-8 rounded-3xl bg-bg-alt/60 border border-text/10 shadow-sm">
        <img
          src={heroImage}
          alt="Career Progress at JobHub"
          className="w-full max-w-md h-auto object-contain transition-transform duration-500 hover:scale-105"
        />
        <div className="mt-4 text-center max-w-sm">
          <span className="text-xs font-semibold text-primary uppercase tracking-wider">Internal Mobility Platform</span>
          <p className="text-sm text-text-alt mt-1">
            Accelerate your growth by applying for open internal roles inside your organization.
          </p>
        </div>
      </div>

      {/* Right side: Header, Subheading, and Login Form */}
      <div className="w-full md:w-1/2 flex flex-col gap-6 p-6 sm:p-10 rounded-3xl bg-bg-alt border border-text/10 shadow-lg">
        {/* Brand Header */}
        <div className="flex flex-col gap-2">
          <Link to="/" className="inline-block w-fit">
            <Logo />
          </Link>
          <p className="text-xs font-medium text-text-alt tracking-wide">
            Discover internal opportunities, find roles that match your skills, and apply in just a few clicks.
          </p>
        </div>

        <hr className="border-text/10" />

        {/* Login Form Organism */}
        <LoginForm onSubmit={handleLoginSubmit} loading={loading} error={error} />
      </div>
    </div>
  );
};

export default Login;
