import { useState } from 'react';
import { ordersApi } from '../services/api';
import { Order } from '../types';

export interface MappedOrder {
  ordernummer: string;
  datum: string;
  thema: string;
  klant: string;
  deadline: string;
  typeOrder: string;
  originalOrder: Order;
}

interface SyncResult {
  new_orders: number;
  skipped_orders: number;
}

export const useFetchOrders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [mappedOrders, setMappedOrders] = useState<MappedOrder[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [syncResult, setSyncResult] = useState<SyncResult | null>(null);

  const fetchOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await ordersApi.getOrders();
      setOrders(data);
      setMappedOrders(mapOrdersToTableData(data));
    } catch (err) {
      console.error('Error fetching orders:', err);
      setError('Fout bij het ophalen van orders');
    } finally {
      setLoading(false);
    }
  };

  const syncOrders = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await ordersApi.syncOrders();
      setSyncResult(result);
      // Fetch updated orders after sync
      await fetchOrders();
    } catch (err) {
      console.error('Error syncing orders:', err);
      setError('Fout bij het synchroniseren van orders');
    } finally {
      setLoading(false);
    }
  };

  const extractThema = (order: Order): string => {
    const customFields: Record<string, string> = {};
    
    // Eerst proberen in products (waar echte data zit)
    for (const product of order.raw_data?.products || []) {
      for (const field of product.custom_field_inputs || []) {
        if (field.label && field.input) {
          customFields[field.label] = field.input;
        }
      }
    }
    
    // Fallback naar root level
    if (Object.keys(customFields).length === 0) {
      for (const field of order.raw_data?.custom_field_inputs || []) {
        const key = field.name || field.label;
        const value = field.value || field.input;
        if (key && value) {
          customFields[key] = value;
        }
      }
    }
    
    // Gebruik backend logic voor thema extractie
    const themaFields = [
      "Vertel over de gelegenheid", 
      "Thema", 
      "Gelegenheid", 
      "Voor welke gelegenheid", 
      "Voor welke gelegenheid?", 
      "Waarvoor is dit lied?", 
      "Gewenste stijl"
    ];
    
    for (const field of themaFields) {
      if (customFields[field]) {
        return customFields[field];
      }
    }
    
    // Fallback naar backend thema veld
    return order.thema || '-';
  };

  const mapOrdersToTableData = (orders: Order[]): MappedOrder[] => {
    return orders.map(order => {
      // Extract thema using new extraction function
      const thema = extractThema(order);

      // Extract klant name
      const klant = order.raw_data?.address?.full_name || 
        (order.raw_data?.address?.firstname && order.raw_data?.address?.lastname ? 
          `${order.raw_data.address.firstname} ${order.raw_data.address.lastname}` : 
          order.klant_naam || '-');

      // Format date
      const datum = order.raw_data?.invoice_date || 
        order.raw_data?.created_at || 
        order.bestel_datum || '';
      
      const formattedDatum = datum ? new Date(datum).toLocaleDateString('nl-NL') : '-';

      return {
        ordernummer: `${order.order_id}`,
        datum: formattedDatum,
        thema,
        klant,
        deadline: '-', // Placeholder for deadline
        typeOrder: order.typeOrder || 'Onbekend',
        originalOrder: order
      };
    });
  };

  return {
    orders,
    mappedOrders,
    loading,
    error,
    syncResult,
    fetchOrders,
    syncOrders
  };
};
