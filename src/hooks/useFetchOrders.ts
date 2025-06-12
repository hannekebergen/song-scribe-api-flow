import { useState } from 'react';
import { Order, OrdersFetchResult } from '../types';

/**
 * Custom hook for fetching orders from the API
 * @returns Object containing loading state, error state, orders data, and fetchOrders function
 */
export function useFetchOrders() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);

  /**
   * Fetches orders from the API
   * @returns Promise resolving to the fetched orders data
   */
  const fetchOrders = async (): Promise<OrdersFetchResult | null> => {
    const apiUrl = import.meta.env.VITE_API_URL;
    const apiKey = import.meta.env.VITE_API_KEY;

    if (!apiUrl || !apiKey) {
      const errorMessage = 'API URL or API Key not defined in environment variables';
      setError(errorMessage);
      return null;
    }

    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${apiUrl}/orders/fetch`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-API-Key': apiKey
        }
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status} ${response.statusText}`);
      }

      const data: OrdersFetchResult = await response.json();
      setOrders(data.orders);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  };

  return {
    loading,
    error,
    orders,
    fetchOrders
  };
}
