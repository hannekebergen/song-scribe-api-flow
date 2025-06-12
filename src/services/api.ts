import axios from 'axios';
import { wakeBackend } from '@/api/wakeBackend';
import { OrdersFetchResult } from '@/types';

// We use the Order interface from types.ts
import { Order } from '@/types';

// Get API URL and key from environment variables with fallbacks
const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://song-scribe-api-flow.onrender.com';
const API_KEY = import.meta.env.VITE_API_KEY || 'jouwsong2025';

// Create axios instance with default configuration
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
  },
});

// Log warning if environment variables are missing
if (!import.meta.env.VITE_API_URL) {
  console.warn('VITE_API_URL is undefined; using fallback:', API_BASE_URL);
}
if (!import.meta.env.VITE_API_KEY) {
  console.warn('VITE_API_KEY is undefined; using fallback');
}

/**
 * API service for orders-related operations
 */
export const ordersApi = {
  /**
   * GET /orders/orders - Fetch all orders
   * @returns Promise resolving to array of orders
   */
  getOrders: () => api.get<Order[]>('/orders/orders').then(r => r.data),

  /**
   * GET /orders/:id - Get order details
   * @param orderId The ID of the order to fetch
   * @returns Promise resolving to the order
   */
  getOrder: (id: number) => api.get<Order>(`/orders/${id}`).then(r => r.data),

  /**
   * POST /orders/:id/regenerate - Regenerate prompt for an order
   * @param orderId The ID of the order to regenerate
   * @returns Promise resolving to the regenerated order
   */
  regeneratePrompt: async (orderId: string): Promise<Order> => {
    try {
      const response = await api.post<Order>(`/orders/${orderId}/regenerate`);
      return response.data;
    } catch (error) {
      console.error('Error regenerating prompt:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to regenerate prompt');
    }
  },

  /**
   * PATCH /orders/:id - Update song text for an order
   * @param orderId The ID of the order to update
   * @param songtekst The new song text
   * @returns Promise resolving to the updated order or null if failed
   */
  updateSongtext: async (orderId: string, songtekst: string): Promise<Order | null> => {
    try {
      const response = await api.patch<Order>(`/orders/${orderId}`, { songtekst });
      return response.data;
    } catch (error) {
      console.error('Error updating songtext:', error);
      return null;
    }
  },

  /**
   * GET /orders/:id/download - Download files for an order
   * @param orderId The ID of the order to download
   * @param type The type of file to download (json or txt)
   * @returns Promise resolving to the file content as a string
   */
  downloadOrder: async (orderId: string, type: 'json' | 'txt'): Promise<string> => {
    try {
      const response = await api.get<string>(`/orders/${orderId}/download?type=${type}`);
      return response.data;
    } catch (error) {
      console.error('Error downloading order:', error);
      return '';
    }
  },

  /**
   * POST /fetch - Fetch new orders from the payment provider
   * @returns Promise resolving to the fetch result
   */
  fetchOrders: () => api.post<{result: OrdersFetchResult}>('/fetch'),
  
  /**
   * Legacy method for backward compatibility
   * @deprecated Use fetchOrders instead
   */
  syncOrders: async (): Promise<OrdersFetchResult> => {
    try {
      // Wake the backend first to avoid cold-start issues
      await wakeBackend();
      
      const response = await api.post<{result: OrdersFetchResult}>('/fetch');
      return response.data.result;
    } catch (error) {
      console.error('Error syncing orders:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to sync orders');
    }
  }
};
