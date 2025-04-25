import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import BlogGenerator from '@/app/blog-generator/page';

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

describe('Blog Generator Page', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders blog generator form correctly', () => {
    render(<BlogGenerator />);
    
    // Check if the form elements are rendered
    expect(screen.getByText('Blog Generator')).toBeInTheDocument();
    expect(screen.getByLabelText('Topic')).toBeInTheDocument();
    expect(screen.getByLabelText('Template Type')).toBeInTheDocument();
    expect(screen.getByLabelText('Storm Type')).toBeInTheDocument();
    expect(screen.getByLabelText('Target Length')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Generate Blog Post' })).toBeInTheDocument();
  });

  it('handles form submission correctly', async () => {
    // Mock successful API response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        success: true, 
        data: {
          title: 'Understanding Hurricane Damage Insurance Claims',
          content: 'This is a mock blog post about insurance claims using the educational template.',
          word_count: 1200,
          seo_score: 85,
          keywords: ['insurance claims', 'storm damage', 'property damage', 'claim process']
        }
      }),
    });

    render(<BlogGenerator />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Topic'), { 
      target: { value: 'Insurance claim process after hurricane damage' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Generate Blog Post' }));
    
    // Check if loading state is shown
    expect(screen.getByTestId('mock-spinner')).toBeInTheDocument();
    
    // Check if fetch was called with correct arguments
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/blog-posts', expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: expect.any(String),
      }));
    });
    
    // Check if the generated content is displayed
    await waitFor(() => {
      expect(screen.getByText('Understanding Hurricane Damage Insurance Claims')).toBeInTheDocument();
    });
  });

  it('handles API errors correctly', async () => {
    // Mock failed API response
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ success: false, error: 'Failed to generate blog post' }),
    });

    render(<BlogGenerator />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Topic'), { 
      target: { value: 'Insurance claim process after hurricane damage' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Generate Blog Post' }));
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to generate blog post')).toBeInTheDocument();
    });
  });
});
