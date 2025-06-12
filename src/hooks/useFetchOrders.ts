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
 * Enriches an order with test data if the fields are missing
 * This is a temporary solution until the backend provides the correct data
 * @param order The raw order to enrich
 * @returns The enriched order
 */
function enrichOrderWithTestData(order: Order): Order {
  // Only enrich if fields are missing
  if (!order.custom_field_inputs) {
    // Add test custom fields based on product name
    const thema = order.product_naam?.includes('Liefde') ? 'Liefde' : 
                 order.product_naam?.includes('Verjaardag') ? 'Verjaardag' : 
                 'Algemeen';
    
    order.custom_field_inputs = [
      { label: 'Gewenste stijl', input: thema },
      { label: 'Andere wensen', input: 'Test wensen' }
    ];
  }
  
  if (!order.products || order.products.length === 0) {
    // Add test products with deadline info
    const isUrgent = order.id % 2 === 0; // Even IDs get urgent delivery
    order.products = [
      { 
        title: isUrgent ? 
          `${order.product_naam} - Binnen ${24 * (order.id % 3 + 1)} uur` : 
          `${order.product_naam} - Standaard levering`
      }
    ];
  }
  
  if (!order.address) {
    // Add test address data
    const nameParts = (order.klant_naam || 'Onbekend').split(' ');
    const firstname = nameParts[0] || 'Voornaam';
    const lastname = nameParts.slice(1).join(' ') || 'Achternaam';
    
    order.address = {
      firstname,
      lastname,
      full_name: order.klant_naam || `${firstname} ${lastname}`
    };
  }
  
  return order;
}

/**
 * Maps a raw order to the display format with datum, thema, klant, and deadline fields
 * @param order The raw order to map
 * @returns The mapped order with display fields
 */
export function mapOrder(order: Order): MappedOrder {
  // First enrich the order with test data if fields are missing
  const enrichedOrder = enrichOrderWithTestData(order);
  
  // Extract deadline from product title using regex
  // Looking for patterns like "Binnen 24 uur" or "Binnen 48 uur"
  let deadline = '';
  try {
    if (enrichedOrder.products && enrichedOrder.products.length > 0) {
      const productTitle = enrichedOrder.products[0].title || '';
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
    if (enrichedOrder.bestel_datum) {
      const date = new Date(enrichedOrder.bestel_datum);
      if (!isNaN(date.getTime())) {
        formattedDate = date.toLocaleDateString();
      }
    }
  } catch (e) {
    console.warn('Error formatting date:', e);
  }

  return {
    ordernummer: enrichedOrder.order_id,
    // Format date as localized string with fallback
    datum: formattedDate,
    // Find the style custom field or use fallback
    thema: enrichedOrder.custom_field_inputs?.find(f => f.label === 'Gewenste stijl')?.input || 'Onbekend',
    // Use full_name if available, otherwise combine firstname and lastname with fallbacks
    klant: enrichedOrder.address?.full_name || 
           (enrichedOrder.address?.firstname || enrichedOrder.address?.lastname ? 
             `${enrichedOrder.address?.firstname || ''} ${enrichedOrder.address?.lastname || ''}`.trim() : 
             enrichedOrder.klant_naam || 'Onbekend'),
    deadline: deadline || 'Standaard',
    originalOrder: enrichedOrder
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
      setOrders(data);
      
      // Map the raw orders to the display format
      const mapped = data.map(mapOrder);
      setMappedOrders(mapped);
      
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
    mappedOrders,
    syncResult,
    fetchOrders,
    syncOrders,
    mapOrder // Export the mapping function for direct use if needed
  };
}
