import React, { useState } from 'react';
import FormField from '../../molecules/FormField/FormField';
import Button from '../../atoms/Button/Button';
import { Mail, Lock, AlertCircle } from 'lucide-react';
import type { LoginFormProps } from '../../../types/loginForm.types';

const LoginForm: React.FC<LoginFormProps> = ({ onSubmit, loading = false, error }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});

  const validate = (): boolean => {
    const newErrors: { email?: string; password?: string } = {};

    if (!email.trim()) {
      newErrors.email = 'Email address is required';
    } else if (!/\S+@\S+\.\S+/.test(email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validate()) return;
    await onSubmit({ email, password });
  };

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col gap-5 bg-bg-alt p-8 md:p-6 rounded-3xl shadow-lg shadow-text/20 border border-text/10 md:min-w-sm md:max-w-md">
      <div className="flex flex-col gap-1">
        <h2 className="text-2xl md:text-3xl font-bold text-primary-hover text-center">Login</h2>
      </div>

      {error && (
        <div className="flex items-center gap-3 p-3.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-600 text-sm font-medium animate-fadeIn">
          <AlertCircle size={18} className="shrink-0 text-red-500" />
          <span>{error}</span>
        </div>
      )}

      <div className="flex flex-col gap-4 opacity-100 z-2 md:z-0">
        <FormField
          label="Email Address"
          type="email"
          name="email"
          placeholder="e.g. tony@jobhub.com"
          value={email}
          onChange={(e) => {
            setEmail(e.target.value);
            if (errors.email) setErrors((prev) => ({ ...prev, email: undefined }));
          }}
          error={errors.email}
          icon={<Mail size={18} />}
          required
        />

        <FormField
          label="Password"
          type="password"
          name="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => {
            setPassword(e.target.value);
            if (errors.password) setErrors((prev) => ({ ...prev, password: undefined }));
          }}
          error={errors.password}
          icon={<Lock size={18} />}
          required
        />
      </div>

      <Button
        type="submit"
        text="Login"
        variant="filled"
        color="primary"
        size="md"
        fullWidth
        loading={loading}
        className="rounded-lg mt-2 font-semibold shadow-md hover:shadow-lg transition-all duration-200"
      />
    </form>
  );
};

export default LoginForm;
