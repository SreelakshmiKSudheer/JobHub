import type { LoginPayload } from './auth.types';

export interface LoginFormProps {
  onSubmit: (payload: LoginPayload) => Promise<void>;
  loading?: boolean;
  error?: string | null;
}
