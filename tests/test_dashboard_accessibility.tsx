import React from 'react';
import { render, screen } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { axe, toHaveNoViolations } from 'jest-axe';
import Dashboard from '../src/components/Dashboard';

// Add the custom matcher
expect.extend(toHaveNoViolations);

// Mock the hooks used in Dashboard
jest.mock('../src/hooks/useFetchOrders', () => ({
  useFetchOrders: () => ({
    mappedOrders: [
      {
        id: 1,
        ordernummer: '12345',
        klantnaam: 'Test Klant',
        bestel_datum: '2025-06-01',
        status: 'Nieuw',
        thema: 'Verjaardag',
        toon: 'Vrolijk',
        structuur: 'Standaard',
        beschrijving: 'Een test beschrijving',
        deadline: '2025-06-30'
      }
    ],
    isLoading: false,
    error: null
  })
}));

describe('Dashboard Component Accessibility', () => {
  it('should render without accessibility violations', async () => {
    const { container } = render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check for accessibility violations
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
  
  it('should have proper aria-labels on select triggers', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check for the aria-labels on the select triggers
    const themaSelect = screen.getByLabelText('Filter op thema');
    expect(themaSelect).toBeInTheDocument();
    
    const statusSelect = screen.getByLabelText('Filter op status');
    expect(statusSelect).toBeInTheDocument();
  });
  
  it('should display orders with the new custom fields', () => {
    render(
      <BrowserRouter>
        <Dashboard />
      </BrowserRouter>
    );
    
    // Check that the new fields are displayed
    expect(screen.getByText('Verjaardag')).toBeInTheDocument();
    expect(screen.getByText('Vrolijk')).toBeInTheDocument();
  });
});
