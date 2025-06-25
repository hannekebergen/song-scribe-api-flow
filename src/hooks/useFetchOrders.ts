import { useState } from 'react';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';
import { getOrderTypeDisplay, isSpeedOrder } from '@/utils/orderTypeDetection';

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
    // Debug logging for development
    if (process.env.NODE_ENV === 'development') {
      console.log(`Mapping order ${order.order_id}:`, {
        order_thema: order.thema,
        order_voornaam: order.voornaam,
        order_klant_naam: order.klant_naam,
        raw_data_address: order.raw_data?.address,
        custom_field_inputs: order.raw_data?.custom_field_inputs?.map(f => ({
          label: f.label || f.name,
          value: f.input || f.value
        })),
        products: order.raw_data?.products?.map(p => ({
          id: p.id,
          title: p.title,
          pivot_type: p.pivot?.type
        }))
      });
    }

    // Enhanced custom field extraction that handles both old and new formats
    const getCustomFieldValue = (...labels: string[]): string => {
      const customFields = order.raw_data?.custom_field_inputs || order.custom_field_inputs || [];
      
      // Try to find field by any of the provided labels
      for (const label of labels) {
        const field = customFields.find(f => {
          // Handle both old format (name/value) and new format (label/input)
          const fieldName = f.label || f.name;
          return fieldName === label;
        });
        
        if (field) {
          // Return input or value depending on format
          return field.input || field.value || '-';
        }
      }
      
      return '-';
    };

    // Enhanced thema extraction with multiple fallback options
    const getThema = (): string => {
      // First try the processed thema field from backend
      if (order.thema && order.thema !== '-') {
        return order.thema;
      }
      
      // Then try various thema field names
      const themaValue = getCustomFieldValue(
        'Thema', 
        'Gelegenheid', 
        'Vertel over de gelegenheid',
        'Voor welke gelegenheid',
        'Voor welke gelegenheid?',
        'Waarvoor is dit lied?',
        'Gewenste stijl'
      );
      
      return themaValue !== '-' ? themaValue : 'Onbekend';
    };

    // Enhanced klant name extraction with multiple fallback options
    const getKlantNaam = (): string => {
      // First try processed fields from backend
      if (order.voornaam && order.voornaam !== '-') {
        return order.voornaam;
      }
      
      if (order.klant_naam && order.klant_naam !== '-') {
        return order.klant_naam;
      }
      
      // Try address fields
      if (order.raw_data?.address?.full_name) {
        return order.raw_data.address.full_name;
      }
      
      if (order.raw_data?.address?.firstname) {
        const firstname = order.raw_data.address.firstname;
        const lastname = order.raw_data?.address?.lastname || '';
        return lastname ? `${firstname} ${lastname}` : firstname;
      }
      
      // Try custom fields
      const voornaamValue = getCustomFieldValue(
        'Voornaam',
        'Naam', 
        'Voor wie is dit lied?',
        'Voor wie'
      );
      
      if (voornaamValue !== '-') {
        const achternaamValue = getCustomFieldValue(
          'Achternaam',
          'Van'
        );
        
        return achternaamValue !== '-' ? `${voornaamValue} ${achternaamValue}` : voornaamValue;
      }
      
      return 'Onbekend';
    };

    // Enhanced deadline detection based on order type
    const getDeadline = (): string => {
      // Check if it's a spoed order
      if (isSpeedOrder(order)) {
        return '24 uur';
      }
      
      // Try custom fields for deadline
      const deadlineValue = getCustomFieldValue('deadline', 'Deadline', 'Wanneer moet het lied klaar zijn?');
      if (deadlineValue !== '-') {
        return deadlineValue;
      }
      
      // Default to standard
      return '72 uur';
    };

    // Use the new order type detection
    const typeOrder = getOrderTypeDisplay(order);

    return {
      ordernummer: order.order_id || order.id,
      datum: new Date(order.bestel_datum).toLocaleDateString('nl-NL'),
      thema: getThema(),
      klant: getKlantNaam(),
      deadline: getDeadline(),
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
