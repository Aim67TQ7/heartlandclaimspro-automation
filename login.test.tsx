import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Login from '@/app/login/page';

// Mock useRouter
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock fetch
global.fetch = jest.fn();

describe('Login Page', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders login form correctly', () => {
    render(<Login />);
    
    // Check if the form elements are rendered
    expect(screen.getByText('Blog Automation System')).toBeInTheDocument();
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign in' })).toBeInTheDocument();
  });

  it('handles form submission correctly on success', async () => {
    // Mock successful login response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ success: true, data: { id: '1', username: 'admin', name: 'Admin User', role: 'admin' } }),
    });

    render(<Login />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'heartland2025' } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
    
    // Check if fetch was called with correct arguments
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: 'admin', password: 'heartland2025' }),
      });
    });
  });

  it('handles form submission correctly on error', async () => {
    // Mock failed login response
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ success: false, error: 'Invalid credentials' }),
    });

    render(<Login />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'admin' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'wrongpassword' } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Sign in' }));
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Invalid credentials')).toBeInTheDocument();
    });
  });
});
