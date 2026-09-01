import { apiClient } from '../apiClient';
import type { ApiResponse } from '../apiClient';
import type { LoginPayload, LoginResponseData } from '../../types/auth.types';

export const authService = {
  login: async (payload: LoginPayload): Promise<LoginResponseData> => {
    const res: ApiResponse<LoginResponseData> = await apiClient<LoginResponseData>('/auth/login', {
      method: 'POST',
      body: JSON.stringify(payload),
    });
    return res.data;
  },

  logout: async (): Promise<void> => {
    try {
      await apiClient<null>('/auth/logout', {
        method: 'POST',
      });
    } catch (err) {
      console.warn('Backend logout call error:', err);
    }
  },
};
