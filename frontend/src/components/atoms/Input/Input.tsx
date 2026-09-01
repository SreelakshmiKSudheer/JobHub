import React, { useState } from 'react';
import type { InputProps } from '../../../types/input.types';
import { Eye, EyeOff } from 'lucide-react';

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  (
    {
      type = 'text',
      label,
      error,
      icon,
      fullWidth = true,
      className = '',
      inputClassName = '',
      containerClassName = '',
      disabled = false,
      id,
      ...props
    },
    ref
  ) => {
    const [showPassword, setShowPassword] = useState(false);
    const isPassword = type === 'password';
    const inputType = isPassword ? (showPassword ? 'text' : 'password') : type;

    const inputId = id || props.name;

    return (
      <div className={`flex flex-col gap-1.5 ${fullWidth ? 'w-full' : 'w-fit'} ${containerClassName}`}>
        {label && (
          <label htmlFor={inputId} className="text-xs font-semibold text-text-alt tracking-wide uppercase">
            {label}
          </label>
        )}
        <div className="relative flex items-center w-full">
          {icon && (
            <div className="absolute left-3.5 text-text-alt pointer-events-none flex items-center justify-center">
              {icon}
            </div>
          )}
          <input
            ref={ref}
            id={inputId}
            type={inputType}
            disabled={disabled}
            className={`
              w-full
              rounded-xl
              border
              bg-bg-alt
              px-4
              py-3.5
              text-sm
              text-text
              placeholder:text-text-alt/50
              outline-none
              transition-all
              duration-200
              ${icon ? 'pl-10' : ''}
              ${isPassword ? 'pr-11' : ''}
              ${
                error
                  ? 'border-red-500 focus:border-red-500 focus:ring-2 focus:ring-red-500/20'
                  : 'border-text/15 hover:border-primary/40 focus:border-primary focus:ring-2 focus:ring-primary/20'
              }
              ${disabled ? 'bg-text/5 cursor-not-allowed opacity-60' : ''}
              ${inputClassName}
              ${className}
            `}
            {...props}
          />
          {isPassword && (
            <button
              type="button"
              onClick={() => setShowPassword((prev) => !prev)}
              tabIndex={-1}
              className="absolute right-3.5 text-text-alt hover:text-primary transition-colors duration-200 p-1 rounded-lg focus:outline-none"
              aria-label={showPassword ? 'Hide password' : 'Show password'}
            >
              {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
            </button>
          )}
        </div>
        {error && <span className="text-xs font-medium text-red-500 mt-0.5">{error}</span>}
      </div>
    );
  }
);

Input.displayName = 'Input';

export default Input;
