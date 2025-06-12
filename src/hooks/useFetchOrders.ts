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
 * Maps a raw order to the display format with datum, thema, klant, and deadline fields
 * @param order The raw order to map
 * @returns The mapped order with display fields
 */
export function mapOrder(order: Order): MappedOrder {
  // Extract deadline from product title using regex
  // Looking for patterns like "Binnen 24 uur" or "Binnen 48 uur"
  let deadline = '';
  try {
    if (order.products && order.products.length > 0) {
      const productTitle = order.products[0].title || '';
      const match = productTitle.match(/Binnen\s+(\d+)\s+uur/i);
      if (match && match[1]) {
        deadline = `${match[1]} uur`;
      }
    }
  } catch (e) {
    console.warn('Error extracting deadline:', e);
  }

  // Safely format date
  let formattedDate = 'Onbekend';
  try {
    if (order.bestel_datum) {
      const date = new Date(order.bestel_datum);
      if (!isNaN(date.getTime())) {
        formattedDate = date.toLocaleDateString();
      }
    }
  } catch (e) {
    console.warn('Error formatting date:', e);
  }

  return {
    ordernummer: order.order_id,
    // Format date as localized string with fallback
    datum: formattedDate,
    // Find the style custom field or use fallback
    thema: order.custom_field_inputs?.find(f => f.label === 'Gewenste stijl')?.input || 'Onbekend',
    // Use full_name if available, otherwise combine firstname and lastname with fallbacks
    klant: order.address?.full_name || 
           (order.address?.firstname || order.address?.lastname ? 
             `${order.address?.firstname || ''} ${order.address?.lastname || ''}`.trim() : 
             order.klant_naam || 'Onbekend'),
    deadline: deadline || 'Standaard',
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
      
      // Store the orders directly without enrichment
      setOrders(data);
      
      // Map the orders to the display format
      const mapped = data.map(mapOrder);
      setMappedOrders(mapped);
      
      // Log the data for debugging
      console.log('Orders from API:', data);
      console.log('Mapped orders:', mapped);
      console.log('⚙️ Mapped orders in hook:', mapped);

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
