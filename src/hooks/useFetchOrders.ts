import { useState } from 'react';
import { Order, OrdersFetchResult } from '../types';
import { ordersApi } from '../services/api';

/**
 * Custom hook for fetching orders from the API
 * @returns Object containing loading state, error state, orders data, fetchOrders function, and syncOrders function
 */
export function useFetchOrders() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [syncResult, setSyncResult] = useState<OrdersFetchResult | null>(null);

  /**
   * Fetches orders from the API using ordersApi.getOrders()
   * @returns Promise resolving to the fetched orders data
   */
  const fetchOrders = async (): Promise<Order[] | null> => {
    setLoading(true);
    setError(null);

    try {
      // Use the ordersApi service to fetch orders
      const data = await ordersApi.getOrders();
      setOrders(data);
      return data;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'An unknown error occurred';
      setError(errorMessage);
      return null;
    } finally {
      setLoading(false);
    }
  };

  /**
   * Syncs new orders from the payment provider using ordersApi.syncOrders()
   * @returns Promise resolving to the sync result
   */
  const syncOrders = async (): Promise<OrdersFetchResult | null> => {
    setLoading(true);
    setError(null);
    setSyncResult(null);

    try {
      // Use the ordersApi service to sync orders
      const result = await ordersApi.syncOrders();
      setSyncResult(result);
      
      // Refresh the orders list after syncing
      await fetchOrders();
      
      return result;
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
    syncResult,
    fetchOrders,
    syncOrders
  };
}
