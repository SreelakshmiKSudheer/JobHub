export interface LoginPayload {
  email: string;
  password: string;
}

export interface LoginResponseData {
  access_token: string;
  token_type: string;
}

export interface UserAuth {
  id: string;
  email: string;
  role: 'admin' | 'user';
}
