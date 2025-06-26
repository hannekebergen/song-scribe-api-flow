
import { useState } from 'react';
import { ordersApi } from '../services/api';
import { Order } from '../types';

export interface MappedOrder {
  ordernummer: string;
  datum: string;
  thema: string;
  klant: string;
  deadline: string;
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

  const mapOrdersToTableData = (orders: Order[]): MappedOrder[] => {
    return orders.map(order => {
      // Extract thema from custom fields
      const thema = order.raw_data?.custom_field_inputs?.find(
        field => field.label === 'Gewenste stijl'
      )?.input || '-';

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
        ordernummer: `#${order.order_id}`,
        datum: formattedDatum,
        thema,
        klant,
        deadline: '-', // Placeholder for deadline
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
