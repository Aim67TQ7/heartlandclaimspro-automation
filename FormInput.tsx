'use client';

import React from 'react';

interface FormInputProps {
  id: string;
  label: string;
  type?: string;
  placeholder?: string;
  value?: string;
  onChange?: (e: React.ChangeEvent<HTMLInputElement>) => void;
  error?: string;
  required?: boolean;
  disabled?: boolean;
  className?: string;
}

export default function FormInput({
  id,
  label,
  type = 'text',
  placeholder = '',
  value,
  onChange,
  error,
  required = false,
  disabled = false,
  className = '',
}: FormInputProps) {
  return (
    <div className={`mb-4 ${className}`}>
      <label 
        htmlFor={id} 
        className="block text-sm font-medium text-gray-dark mb-1"
      >
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <input
        id={id}
        name={id}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        disabled={disabled}
        required={required}
        className={`w-full px-3 py-2 border ${
          error ? 'border-red-500' : 'border-gray-300'
        } rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-primary focus:border-primary transition-colors duration-200 ${
          disabled ? 'bg-gray-100 cursor-not-allowed' : ''
        }`}
      />
      {error && (
        <p className="mt-1 text-sm text-red-500">{error}</p>
      )}
    </div>
  );
}
