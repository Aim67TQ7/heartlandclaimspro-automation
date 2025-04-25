import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import UserManagement from '@/app/admin/users/page';

// Mock useRouter
jest.mock('next/navigation', () => ({
  useRouter: () => ({
    push: jest.fn(),
  }),
}));

// Mock fetch
global.fetch = jest.fn();

// Mock components
jest.mock('@/components/Layout', () => {
  return function MockLayout({ children }) {
    return <div data-testid="mock-layout">{children}</div>;
  };
});

jest.mock('@/components/LoadingSpinner', () => {
  return function MockLoadingSpinner() {
    return <div data-testid="mock-spinner">Loading...</div>;
  };
});

describe('User Management Page', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders loading state initially', () => {
    render(<UserManagement />);
    
    // Check if loading spinner is shown
    expect(screen.getByTestId('mock-spinner')).toBeInTheDocument();
    expect(screen.getByText('Loading users...')).toBeInTheDocument();
  });

  it('renders user list after loading', async () => {
    render(<UserManagement />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading users...')).not.toBeInTheDocument();
    });
    
    // Check if user management content is rendered
    expect(screen.getByText('User Management')).toBeInTheDocument();
    expect(screen.getByText('System Users')).toBeInTheDocument();
    expect(screen.getByText('Admin User')).toBeInTheDocument();
    expect(screen.getByText('John Editor')).toBeInTheDocument();
    expect(screen.getByText('Sarah Writer')).toBeInTheDocument();
  });

  it('shows add user form when button is clicked', async () => {
    render(<UserManagement />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading users...')).not.toBeInTheDocument();
    });
    
    // Click the Add New User button
    fireEvent.click(screen.getByRole('button', { name: 'Add New User' }));
    
    // Check if the form is displayed
    expect(screen.getByText('Add New User')).toBeInTheDocument();
    expect(screen.getByLabelText('Username')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByLabelText('Full Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Email')).toBeInTheDocument();
    expect(screen.getByLabelText('Role')).toBeInTheDocument();
  });

  it('adds a new user successfully', async () => {
    render(<UserManagement />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading users...')).not.toBeInTheDocument();
    });
    
    // Click the Add New User button
    fireEvent.click(screen.getByRole('button', { name: 'Add New User' }));
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Username'), { target: { value: 'newuser' } });
    fireEvent.change(screen.getByLabelText('Password'), { target: { value: 'password123' } });
    fireEvent.change(screen.getByLabelText('Full Name'), { target: { value: 'New Test User' } });
    fireEvent.change(screen.getByLabelText('Email'), { target: { value: 'newuser@example.com' } });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Add User' }));
    
    // Check if success message is displayed
    await waitFor(() => {
      expect(screen.getByText('User New Test User added successfully')).toBeInTheDocument();
    });
    
    // Check if the new user is added to the table
    expect(screen.getByText('New Test User')).toBeInTheDocument();
  });

  it('displays role permissions information', async () => {
    render(<UserManagement />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading users...')).not.toBeInTheDocument();
    });
    
    // Check if role permissions section is displayed
    expect(screen.getByText('Role Permissions')).toBeInTheDocument();
    expect(screen.getByText('Administrator')).toBeInTheDocument();
    expect(screen.getByText('Editor')).toBeInTheDocument();
    expect(screen.getByText('Writer')).toBeInTheDocument();
    
    // Check specific permissions
    expect(screen.getByText('Manage Users')).toBeInTheDocument();
    expect(screen.getByText('System Settings')).toBeInTheDocument();
    expect(screen.getByText('Generate Content')).toBeInTheDocument();
    expect(screen.getByText('Publish Content')).toBeInTheDocument();
  });
});
