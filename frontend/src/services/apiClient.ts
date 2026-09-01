import { getCookie } from '../utils/cookies';

const API_BASE_URL = 'http://localhost:8000/v1';

export interface ApiResponse<T = any> {
  status_code: number;
  message: string;
  data: T;
  error?: string | null;
}

export async function apiClient<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<ApiResponse<T>> {
  const token = getCookie('access_token');

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  const responseData: ApiResponse<T> = await response.json();

  if (!response.ok) {
    const errorMsg = responseData.error || responseData.message || 'API request failed';
    throw new Error(errorMsg);
  }

  return responseData;
}
