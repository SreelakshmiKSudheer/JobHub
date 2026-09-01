import React from 'react';
import Input from '../../atoms/Input/Input';
import type { FormFieldProps } from '../../../types/formField.types';

const FormField: React.FC<FormFieldProps> = ({ label, error, helperText, ...props }) => {
  return (
    <div className="w-full flex flex-col">
      <Input label={label} error={error} {...props} />
      {helperText && !error && (
        <span className="text-xs text-text-alt mt-1">{helperText}</span>
      )}
    </div>
  );
};

export default FormField;
