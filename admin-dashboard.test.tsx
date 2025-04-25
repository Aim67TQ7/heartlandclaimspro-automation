import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import AdminDashboard from '@/app/admin/page';

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

describe('Admin Dashboard Page', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders loading state initially', () => {
    render(<AdminDashboard />);
    
    // Check if loading spinner is shown
    expect(screen.getByTestId('mock-spinner')).toBeInTheDocument();
    expect(screen.getByText('Loading dashboard data...')).toBeInTheDocument();
  });

  it('renders dashboard content after loading', async () => {
    render(<AdminDashboard />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading dashboard data...')).not.toBeInTheDocument();
    });
    
    // Check if dashboard content is rendered
    expect(screen.getByText('Admin Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Total Blog Posts')).toBeInTheDocument();
    expect(screen.getByText('Published')).toBeInTheDocument();
    expect(screen.getByText('Scheduled')).toBeInTheDocument();
    expect(screen.getByText('Drafts')).toBeInTheDocument();
    expect(screen.getByText('Avg. SEO Score')).toBeInTheDocument();
    expect(screen.getByText('Recent Activity')).toBeInTheDocument();
    expect(screen.getByText('Quick Actions')).toBeInTheDocument();
  });

  it('displays correct statistics', async () => {
    render(<AdminDashboard />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading dashboard data...')).not.toBeInTheDocument();
    });
    
    // Check if statistics are displayed correctly
    expect(screen.getByText('12')).toBeInTheDocument(); // Total posts
    expect(screen.getByText('4')).toBeInTheDocument(); // Published posts
    expect(screen.getByText('3')).toBeInTheDocument(); // Scheduled posts
    expect(screen.getByText('5')).toBeInTheDocument(); // Draft posts
    expect(screen.getByText('84')).toBeInTheDocument(); // Avg SEO score
  });

  it('displays recent activity', async () => {
    render(<AdminDashboard />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading dashboard data...')).not.toBeInTheDocument();
    });
    
    // Check if recent activity is displayed
    expect(screen.getByText('Understanding Insurance Claims After Hurricane Damage')).toBeInTheDocument();
    expect(screen.getByText('How to Document Storm Damage for Maximum Claim Value')).toBeInTheDocument();
    expect(screen.getByText('Working with Public Adjusters: What You Need to Know')).toBeInTheDocument();
  });

  it('has working quick action buttons', async () => {
    render(<AdminDashboard />);
    
    // Wait for the simulated data loading to complete
    await waitFor(() => {
      expect(screen.queryByText('Loading dashboard data...')).not.toBeInTheDocument();
    });
    
    // Check if quick action buttons are rendered
    expect(screen.getByRole('button', { name: 'Generate New Blog Post' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Publish Pending Posts' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'View Scheduled Posts' })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Test Content Quality' })).toBeInTheDocument();
  });
});
