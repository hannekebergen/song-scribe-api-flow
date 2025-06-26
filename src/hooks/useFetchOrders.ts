import { useState } from 'react';
import { ordersApi } from '../services/api';
import { Order } from '../types';
import { detectOrderType } from '@/utils/orderTypeDetection';

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

  const extractThema = (order: Order, allOrders: Order[]): string => {
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
    if (order.thema && order.thema !== '-') {
      return order.thema;
    }
    
    // Voor upsell orders: probeer thema van originele order over te nemen
    const orderType = detectOrderType(order);
    if (orderType.badge === 'upsell' && order.origin_song_id) {
      const originalOrder = allOrders.find(o => o.order_id === order.origin_song_id);
      if (originalOrder) {
        const originalThema = extractThema(originalOrder, []);
        if (originalThema && originalThema !== '-') {
          console.log(`Thema '${originalThema}' overgenomen van originele order ${order.origin_song_id} voor upsell ${order.order_id}`);
          return originalThema;
        }
      }
    }
    
    // Als upsell order geen origin_song_id heeft, zoek naar vergelijkbare orders van dezelfde klant
    if (orderType.badge === 'upsell' && order.klant_email) {
      const orderDate = new Date(order.bestel_datum);
      const dayBefore = new Date(orderDate.getTime() - 24 * 60 * 60 * 1000); // 24 uur eerder
      
      const possibleOriginals = allOrders.filter(o => {
        if (o.order_id === order.order_id) return false; // Niet zichzelf
        if (o.klant_email !== order.klant_email) return false; // Zelfde klant
        
        const otherDate = new Date(o.bestel_datum);
        if (otherDate < dayBefore || otherDate >= orderDate) return false; // Binnen 24 uur voor upsell
        
        const otherType = detectOrderType(o);
        return otherType.badge === 'standaard' || otherType.badge === 'spoed'; // Alleen standaard orders
      });
      
      if (possibleOriginals.length > 0) {
        // Neem de meest recente
        const mostRecent = possibleOriginals.sort((a, b) => 
          new Date(b.bestel_datum).getTime() - new Date(a.bestel_datum).getTime()
        )[0];
        
        const inheritedThema = extractThema(mostRecent, []);
        if (inheritedThema && inheritedThema !== '-') {
          console.log(`Thema '${inheritedThema}' overgenomen van order ${mostRecent.order_id} voor upsell ${order.order_id} op basis van klant matching`);
          return inheritedThema;
        }
      }
    }
    
    return '-';
  };

  const getOrderTypeDisplay = (order: Order): string => {
    // Eerst proberen backend typeOrder
    if (order.typeOrder && order.typeOrder !== 'Onbekend') {
      return order.typeOrder;
    }
    
    // Fallback naar frontend detectie
    const detectedType = detectOrderType(order);
    return detectedType.type;
  };

  const mapOrdersToTableData = (orders: Order[]): MappedOrder[] => {
    return orders.map(order => {
      // Extract thema using new extraction function with access to all orders
      const thema = extractThema(order, orders);

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

      // Get order type with frontend fallback
      const typeOrder = getOrderTypeDisplay(order);

      return {
        ordernummer: `${order.order_id}`,
        datum: formattedDatum,
        thema,
        klant,
        deadline: '-', // Placeholder for deadline
        typeOrder,
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
