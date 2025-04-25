import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import ContentTester from '@/app/content-tester/page';

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

describe('Content Tester Page', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  it('renders content tester form correctly', () => {
    render(<ContentTester />);
    
    // Check if the form elements are rendered
    expect(screen.getByText('Content Tester')).toBeInTheDocument();
    expect(screen.getByLabelText('Content Source')).toBeInTheDocument();
    expect(screen.getByLabelText('Blog Content')).toBeInTheDocument();
    expect(screen.getByLabelText('Target Keywords')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Analyze Content' })).toBeInTheDocument();
  });

  it('handles form submission correctly', async () => {
    // Mock successful API response
    fetch.mockResolvedValueOnce({
      ok: true,
      json: async () => ({ 
        success: true, 
        data: {
          seo_score: 72,
          readability_score: "B+",
          keyword_density: 1.8,
          detected_keywords: ["insurance claims", "storm damage", "property damage", "claim process", "insurance adjuster"],
          suggestions: [
            "Add more content to reach recommended length",
            "Optimize title with target keywords",
            "Add more transition words"
          ]
        }
      }),
    });

    render(<ContentTester />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Blog Content'), { 
      target: { value: 'This is a test blog post about insurance claims after storm damage.' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Analyze Content' }));
    
    // Check if loading state is shown
    expect(screen.getByTestId('mock-spinner')).toBeInTheDocument();
    
    // Check if fetch was called with correct arguments
    await waitFor(() => {
      expect(fetch).toHaveBeenCalledWith('/api/test', expect.objectContaining({
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: expect.any(String),
      }));
    });
    
    // Check if the analysis results are displayed
    await waitFor(() => {
      expect(screen.getByText('SEO Score: Good')).toBeInTheDocument();
      expect(screen.getByText('Detected Keywords')).toBeInTheDocument();
      expect(screen.getByText('Keyword Density')).toBeInTheDocument();
    });
  });

  it('disables analyze button when content is empty', () => {
    render(<ContentTester />);
    
    // Check if the button is disabled
    expect(screen.getByRole('button', { name: 'Analyze Content' })).toBeDisabled();
    
    // Add content
    fireEvent.change(screen.getByLabelText('Blog Content'), { 
      target: { value: 'This is a test blog post.' } 
    });
    
    // Check if the button is enabled
    expect(screen.getByRole('button', { name: 'Analyze Content' })).toBeEnabled();
  });

  it('handles API errors correctly', async () => {
    // Mock failed API response
    fetch.mockResolvedValueOnce({
      ok: false,
      json: async () => ({ success: false, error: 'Failed to analyze content' }),
    });

    render(<ContentTester />);
    
    // Fill in the form
    fireEvent.change(screen.getByLabelText('Blog Content'), { 
      target: { value: 'This is a test blog post about insurance claims.' } 
    });
    
    // Submit the form
    fireEvent.click(screen.getByRole('button', { name: 'Analyze Content' }));
    
    // Check if error message is displayed
    await waitFor(() => {
      expect(screen.getByText('Failed to analyze content')).toBeInTheDocument();
    });
  });
});
