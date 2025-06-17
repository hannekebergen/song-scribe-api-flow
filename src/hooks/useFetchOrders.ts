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
  let deadline = 'Standaard';
  try {
    // Get deadline from raw_data.products[0].title
    if (order.raw_data?.products && order.raw_data.products.length > 0) {
      const productTitle = order.raw_data.products[0].title || '';
      const match = productTitle.match(/Binnen\s+(\d+)\s+uur/i);
      if (match && match[1]) {
        deadline = `${match[1]} uur`;
      }
    }
  } catch (e) {
    console.warn('Error extracting deadline from raw_data:', e);
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

  // Extract thema from raw_data.custom_field_inputs
  let thema = 'Onbekend';
  try {
    thema = order.raw_data?.custom_field_inputs?.find(f => f.label === 'Gewenste stijl')?.input || 'Onbekend';
  } catch (e) {
    console.warn('Error extracting thema from raw_data:', e);
  }

  // Extract klant from raw_data.address
  let klant = 'Onbekend';
  try {
    klant = order.raw_data?.address?.full_name || 
           (order.raw_data?.address?.firstname || order.raw_data?.address?.lastname ? 
             `${order.raw_data?.address?.firstname || ''} ${order.raw_data?.address?.lastname || ''}`.trim() : 
             'Onbekend');
  } catch (e) {
    console.warn('Error extracting klant from raw_data:', e);
  }

  return {
    ordernummer: order.order_id,
    datum: formattedDate,
    thema: thema,
    klant: klant,
    deadline: deadline,
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
