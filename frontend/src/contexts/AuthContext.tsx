import React, { createContext, useContext, useEffect, useState } from 'react';
import type { LoginPayload, UserAuth } from '../types/auth.types';
import { authService } from '../services/auth/authService';
import { getCookie, removeCookie, setCookie } from '../utils/cookies';
import { decodeJwt, isTokenExpired } from '../utils/jwt';

interface AuthContextType {
  token: string | null;
  role: 'admin' | 'user' | null;
  user: UserAuth | null;
  isAuthenticated: boolean;
  loading: boolean;
  login: (payload: LoginPayload) => Promise<'admin' | 'user'>;
  logout: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [token, setToken] = useState<string | null>(null);
  const [role, setRole] = useState<'admin' | 'user' | null>(null);
  const [user, setUser] = useState<UserAuth | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const savedToken = getCookie('access_token');
    if (savedToken && !isTokenExpired(savedToken)) {
      const decoded = decodeJwt(savedToken);
      if (decoded && decoded.role) {
        setToken(savedToken);
        setRole(decoded.role);
        setUser({ id: decoded.sub, email: '', role: decoded.role });
      } else {
        removeCookie('access_token');
      }
    } else if (savedToken) {
      removeCookie('access_token');
    }
    setLoading(false);
  }, []);

  const login = async (payload: LoginPayload): Promise<'admin' | 'user'> => {
    const data = await authService.login(payload);
    const accessToken = data.access_token;
    setCookie('access_token', accessToken, 0, 30);

    const decoded = decodeJwt(accessToken);
    if (!decoded || !decoded.role) {
      throw new Error('Invalid token received from server');
    }

    setToken(accessToken);
    setRole(decoded.role);
    setUser({ id: decoded.sub, email: payload.email, role: decoded.role });

    return decoded.role;
  };

  const logout = async () => {
    await authService.logout();
    removeCookie('access_token');
    setToken(null);
    setRole(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        token,
        role,
        user,
        isAuthenticated: !!token && !!role,
        loading,
        login,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
