import type { InputProps } from './input.types';

export interface FormFieldProps extends InputProps {
  label: string;
  helperText?: string;
}
