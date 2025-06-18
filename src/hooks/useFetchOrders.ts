
import { useState } from 'react';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';

export interface MappedOrder {
  ordernummer: number | undefined;
  datum: string;
  thema: string;
  klant: string;
  deadline: string;
  typeOrder: string;
  originalOrder: Order;
}

export const useFetchOrders = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchOrders = async () => {
    setLoading(true);
    try {
      const fetchedOrders = await ordersApi.getOrders();
      setOrders(fetchedOrders);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const mapOrderToDisplay = (order: Order): MappedOrder => {
    // Extract custom field values safely
    const getCustomFieldValue = (label: string): string => {
      const customFields = order.raw_data?.custom_field_inputs || order.custom_field_inputs || [];
      const field = customFields.find(f => f.label === label);
      return field?.input || '-';
    };

    // Create a synthetic deadline field for spoed detection
    const deadline = getCustomFieldValue('deadline') || 'standaard';
    
    // Determine order type based on available data
    const typeOrder = order.songtekst ? 'Songtekst' : 'Prompt';

    return {
      ordernummer: order.order_id || order.id,
      datum: new Date(order.bestel_datum).toLocaleDateString('nl-NL'),
      thema: order.thema || getCustomFieldValue('Thema') || 'Onbekend',
      klant: order.voornaam || order.klant_naam || order.raw_data?.address?.firstname || 'Onbekend',
      deadline,
      typeOrder,
      originalOrder: order
    };
  };

  const mappedOrders = orders.map(mapOrderToDisplay);

  return {
    orders,
    mappedOrders,
    loading,
    fetchOrders
  };
};
