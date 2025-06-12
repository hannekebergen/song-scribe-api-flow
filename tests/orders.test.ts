import { describe, it, expect, vi, beforeEach } from 'vitest';
import { ordersApi } from '../src/services/api';
import { wakeBackend } from '../src/api/wakeBackend';
import axios from 'axios';

// Add type declarations for vitest mocking
type MockedFunction<T extends (...args: any) => any> = T & { mockResolvedValueOnce: any, mockRejectedValueOnce: any };

// Mock dependencies
vi.mock('axios');
vi.mock('../src/api/wakeBackend', () => ({
  wakeBackend: vi.fn().mockResolvedValue(undefined)
}));

describe('Orders API Service', () => {
  const mockOrders = [
    {
      id: 1,
      order_id: 202540,
      klant_naam: 'Test Klant',
      klant_email: 'test@example.com',
      product_naam: 'Songtekst Verjaardag',
      bestel_datum: '2024-01-15'
    },
    {
      id: 2,
      order_id: 202541,
      klant_naam: 'Andere Klant',
      klant_email: 'andere@example.com',
      product_naam: 'Songtekst Liefde',
      bestel_datum: '2024-01-16'
    }
  ];

  beforeEach(() => {
    vi.clearAllMocks();
  });

  describe('getOrders', () => {
    it('should fetch orders successfully', async () => {
      // Setup mock response
      const mockedAxios = axios as any;
      mockedAxios.get = vi.fn().mockResolvedValueOnce({ data: mockOrders });

      // Call the function
      const result = await ordersApi.getOrders();

      // Verify wakeBackend was called
      expect(wakeBackend).toHaveBeenCalledTimes(1);

      // Verify axios.get was called with correct parameters
      expect(mockedAxios.get).toHaveBeenCalledWith('/orders/orders');

      // Verify the result matches our mock data
      expect(result).toEqual(mockOrders);
      expect(result.length).toBe(2);
      expect(result[0].order_id).toBe(202540);
    });

    it('should throw an error when the API call fails', async () => {
      // Setup mock error response
      const errorMessage = 'Network Error';
      const mockedAxios = axios as any;
      mockedAxios.get = vi.fn().mockRejectedValueOnce(new Error(errorMessage));

      // Verify that the function throws an error
      await expect(ordersApi.getOrders()).rejects.toThrow();

      // Verify wakeBackend was called
      expect(wakeBackend).toHaveBeenCalledTimes(1);

      // Verify axios.get was called
      expect(mockedAxios.get).toHaveBeenCalledWith('/orders/orders');
    });
  });

  describe('syncOrders', () => {
    it('should sync orders successfully', async () => {
      // Setup mock response
      const mockResult = {
        new_orders: 2,
        skipped_orders: 1,
        orders: mockOrders
      };
      
      const mockedAxios = axios as any;
      mockedAxios.post = vi.fn().mockResolvedValueOnce({ 
        data: { 
          result: mockResult 
        } 
      });

      // Call the function
      const result = await ordersApi.syncOrders();

      // Verify wakeBackend was called
      expect(wakeBackend).toHaveBeenCalledTimes(1);

      // Verify axios.post was called with correct parameters
      expect(mockedAxios.post).toHaveBeenCalledWith('/fetch');

      // Verify the result matches our mock data
      expect(result).toEqual(mockResult);
      expect(result.new_orders).toBe(2);
      expect(result.skipped_orders).toBe(1);
    });

    it('should throw an error when the sync API call fails', async () => {
      // Setup mock error response
      const errorMessage = 'Network Error';
      const mockedAxios = axios as any;
      mockedAxios.post = vi.fn().mockRejectedValueOnce(new Error(errorMessage));

      // Verify that the function throws an error
      await expect(ordersApi.syncOrders()).rejects.toThrow();

      // Verify wakeBackend was called
      expect(wakeBackend).toHaveBeenCalledTimes(1);

      // Verify axios.post was called
      expect(mockedAxios.post).toHaveBeenCalledWith('/fetch');
    });
  });
});
