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

    // Enhanced custom field extraction - AANGEPAST voor echte API data (2025-06-25)
    const getCustomFieldValue = (...labels: string[]): string => {
      // Eerst proberen in products (waar de echte data zit!)
      if (order.raw_data?.products) {
        for (const product of order.raw_data.products) {
          if (product.custom_field_inputs) {
            for (const field of product.custom_field_inputs) {
              if (labels.includes(field.label || '')) {
                return field.input || '-';
              }
            }
          }
        }
      }
      
      // Fallback naar root level (legacy)
      const customFields = order.raw_data?.custom_field_inputs || order.custom_field_inputs || [];
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
      
      // Then try various thema field names - AANGEPAST voor echte API data
      const themaValue = getCustomFieldValue(
        'Vertel over de gelegenheid',  // Echte veldnaam uit API data
        'Thema', 
        'Gelegenheid', 
        'Voor welke gelegenheid',
        'Voor welke gelegenheid?',
        'Waarvoor is dit lied?',
        'Gewenste stijl'
      );
      
      if (themaValue !== '-') {
        return themaValue;
      }
      
      // Voor UpSell orders: probeer thema van originele order op te halen
      const orderTypeInfo = getOrderTypeDisplay(order);
      if (orderTypeInfo.includes('Upsell') || orderTypeInfo.includes('Extra') || orderTypeInfo.includes('Soundtrack')) {
        // Als dit een UpSell is maar geen thema heeft, probeer van originele order
        if (order.origin_song_id) {
          // Zoek de originele order in de orders array
          const originalOrder = orders.find(o => o.order_id === order.origin_song_id);
          if (originalOrder && originalOrder.thema && originalOrder.thema !== '-') {
            return `${originalOrder.thema} (van originele order)`;
          }
        }
        
        // Als we geen originele order kunnen vinden, probeer op basis van klant en datum
        const customerName = getKlantNaam();
        if (customerName !== 'Onbekend') {
          // Zoek naar een recente standaard order van dezelfde klant
          const recentStandardOrders = orders
            .filter(o => {
              const otherCustomerName = getCustomerNameForOrder(o);
              const isStandard = o.raw_data?.products?.some(p => 
                [274588, 289456].includes(p.id) && p.pivot?.type !== 'upsell'
              );
              const orderDate = new Date(o.bestel_datum);
              const currentDate = new Date(order.bestel_datum);
              const hoursDiff = (currentDate.getTime() - orderDate.getTime()) / (1000 * 60 * 60);
              
              return isStandard && 
                     otherCustomerName === customerName && 
                     hoursDiff >= 0 && 
                     hoursDiff <= 24; // Binnen 24 uur
            })
            .sort((a, b) => new Date(b.bestel_datum).getTime() - new Date(a.bestel_datum).getTime());
          
          if (recentStandardOrders.length > 0 && recentStandardOrders[0].thema) {
            return `${recentStandardOrders[0].thema} (overgenomen)`;
          }
        }
      }
      
      return 'Onbekend';
    };
    
    // Helper functie om klantnaam voor een andere order op te halen
    const getCustomerNameForOrder = (otherOrder: Order): string => {
      if (otherOrder.voornaam && otherOrder.voornaam !== '-' && otherOrder.voornaam.trim() && otherOrder.voornaam !== 'null') {
        return otherOrder.voornaam;
      }
      
      if (otherOrder.klant_naam && otherOrder.klant_naam !== '-' && otherOrder.klant_naam.trim() && otherOrder.klant_naam !== 'null') {
        return otherOrder.klant_naam;
      }
      
      if (otherOrder.raw_data?.address?.full_name && otherOrder.raw_data.address.full_name.trim()) {
        return otherOrder.raw_data.address.full_name;
      }
      
      return 'Onbekend';
    };

    // VERBETERDE klantnaam extractie met uitgebreide fallback logica
    const getKlantNaam = (): string => {
      // Stap 1: Probeer backend verwerkte velden eerst
      if (order.voornaam && order.voornaam !== '-' && order.voornaam.trim() && order.voornaam !== 'null') {
        return order.voornaam;
      }
      
      if (order.klant_naam && order.klant_naam !== '-' && order.klant_naam.trim() && order.klant_naam !== 'null') {
        return order.klant_naam;
      }
      
      // Stap 2: Probeer address velden uit raw_data
      if (order.raw_data?.address?.full_name && order.raw_data.address.full_name.trim()) {
        return order.raw_data.address.full_name;
      }
      
      if (order.raw_data?.address?.firstname && order.raw_data.address.firstname.trim()) {
        const firstname = order.raw_data.address.firstname.trim();
        const lastname = order.raw_data?.address?.lastname?.trim() || '';
        return lastname ? `${firstname} ${lastname}` : firstname;
      }
      
      // Stap 3: Probeer customer velden uit raw_data
      if (order.raw_data?.customer?.name && order.raw_data.customer.name.trim()) {
        return order.raw_data.customer.name;
      }
      
      // Stap 4: Probeer custom fields - uitgebreide lijst met alle mogelijke varianten
      const voornaamValue = getCustomFieldValue(
        'Voornaam',
        'Voor wie is dit lied?',
        'Voor wie',
        'Naam',
        'Voor wie is het lied?',
        'Wie is de ontvanger?',
        'Naam ontvanger',
        'Klant naam'
      );
      
      if (voornaamValue && voornaamValue !== '-' && voornaamValue.trim()) {
        const achternaamValue = getCustomFieldValue(
          'Achternaam',
          'Van',
          'Familienaam',
          'Laatste naam'
        );
        
        const voornaam = voornaamValue.trim();
        const achternaam = achternaamValue && achternaamValue !== '-' ? achternaamValue.trim() : '';
        
        return achternaam ? `${voornaam} ${achternaam}` : voornaam;
      }
      
      // Stap 5: Probeer beschrijving velden voor namen (soms staat de naam in de beschrijving)
      const beschrijvingValue = getCustomFieldValue(
        'Beschrijf',
        'Persoonlijk verhaal',
        'Vertel over de persoon',
        'Toelichting'
      );
      
      if (beschrijvingValue && beschrijvingValue !== '-' && beschrijvingValue.trim()) {
        const beschrijving = beschrijvingValue.trim();
        // Probeer een naam te extraheren uit de eerste zin (vaak begint met de naam)
        const firstSentence = beschrijving.split('.')[0];
        const words = firstSentence.split(' ');
        
        // Als de eerste 2-3 woorden lijken op een naam (hoofdletters), gebruik die
        if (words.length >= 2) {
          const potentialName = words.slice(0, 2).join(' ');
          // Check of het begint met hoofdletters (waarschijnlijk een naam)
          if (/^[A-Z][a-z]+ [A-Z][a-z]+/.test(potentialName)) {
            return potentialName;
          }
          // Of alleen de eerste naam als het één woord met hoofdletter is
          if (/^[A-Z][a-z]+/.test(words[0]) && words[0].length > 2) {
            return words[0];
          }
        }
      }
      
      // Stap 6: Laatste poging - kijk naar product titel of andere velden
      if (order.raw_data?.products && order.raw_data.products.length > 0) {
        const product = order.raw_data.products[0];
        if (product.title && product.title.includes('voor ')) {
          const match = product.title.match(/voor ([A-Z][a-z]+(?: [A-Z][a-z]+)?)/);
          if (match) {
            return match[1];
          }
        }
      }
      
      // Als we hier komen, hebben we geen naam kunnen vinden
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
