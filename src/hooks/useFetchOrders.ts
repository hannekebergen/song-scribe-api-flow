import { useState } from 'react';
import { Order, OrdersFetchResult } from '../types';
import { ordersApi } from '../services/api';

/**
 * Interface for mapped order data with specific display fields
 */
export interface MappedOrder {
  ordernummer: number;
  datum: string;
  thema: string;
  klant: string;
  deadline: string;
  originalOrder: Order; // Keep reference to original order
}

/**
 * Custom hook for fetching orders from the API
 * @returns Object containing loading state, error state, orders data, fetchOrders function, and syncOrders function
 */
/**
 * Maps a raw order to the display format with datum, thema, klant, and deadline fields
 * @param order The raw order to map
 * @returns The mapped order with display fields
 */

/**
 * Helper function to find a custom field value by multiple possible keys
 * @param order The order object
 * @param keys Array of possible field names to look for
 * @returns The found value or a default value
 */
const cf = (order: Order, ...keys: string[]): string => {
  if (!order.raw_data?.custom_field_inputs) return '-';
  
  const field = order.raw_data.custom_field_inputs.find(
    (f: any) => keys.includes(f.name || f.label)
  );
  
  return (field?.value || field?.input || '-');
};

/**
 * Maps a raw order to the display format with datum, thema, klant, and deadline fields
 * @param order The raw order to map
 * @returns The mapped order with display fields
 */
export function mapOrder(order: Order): MappedOrder {
  // Format date from invoice_date or created_at
  const formattedDate = new Date(order.raw_data?.invoice_date || order.raw_data?.created_at || order.bestel_datum).toLocaleDateString('nl-NL');

  // Use the API-derived fields with fallback to custom fields
  const thema = order.thema || cf(order, 'Vertel over de gelegenheid', 'Gewenste stijl', 'Thema');
  
  // Use the API-derived fields with fallback to custom fields
  const toon = order.toon || cf(order, 'Toon', 'Sfeer');
  
  // Extract klant name with multiple fallbacks
  const klant = order.klant_naam || 
                order.raw_data?.address?.full_name || 
                (order.raw_data?.address?.firstname && order.raw_data?.address?.lastname ? 
                 `${order.raw_data.address.firstname} ${order.raw_data.address.lastname}` : '-');
  
  // Use the API-derived deadline or extract from product title
  let deadline = order.deadline;
  if (!deadline && order.raw_data?.products?.[0]?.title) {
    const match = order.raw_data.products[0].title.match(/Binnen\s+(\d+)\s+uur/);
    if (match) {
      deadline = match[1] + ' uur';
    }
  }

  return {
    ordernummer: order.order_id,
    datum: formattedDate,
    thema: thema || '-',
    klant: klant || '-',
    deadline: deadline || '-',
    originalOrder: order
  };
}

export function useFetchOrders() {
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [orders, setOrders] = useState<Order[]>([]);
  const [mappedOrders, setMappedOrders] = useState<MappedOrder[]>([]);
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
      
      // Store the orders directly
      setOrders(data);
      
      // Map the orders to the display format
      const mapped = data.map(mapOrder);
      setMappedOrders(mapped);
      
      return data;
    } catch (error: any) {
      console.error('Error fetching orders:', error);
      setError(error?.message || 'Er is een fout opgetreden bij het ophalen van de bestellingen');
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
    mappedOrders,
    syncResult,
    fetchOrders,
    syncOrders,
    mapOrder // Export the mapping function for direct use if needed
  };
}
