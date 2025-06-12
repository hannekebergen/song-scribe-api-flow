import { useState, useEffect } from 'react';
import { Order } from '@/types';
import { ordersApi } from '@/services/api';

/**
 * Hook to fetch a single order by ID
 * @param id The order ID to fetch
 * @returns Object containing the order, loading state, and error
 */
export function useOrder(id: number) {
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoad] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let isMounted = true;
    
    const fetchOrder = async () => {
      try {
        const data = await ordersApi.getOrder(id);
        if (isMounted) setOrder(data);
      } catch (e) {
        if (isMounted) setError(e instanceof Error ? e.message : 'Error fetching order');
      } finally {
        if (isMounted) setLoad(false);
      }
    };
    
    fetchOrder();
    
    // Cleanup function to prevent state updates on unmounted component
    return () => { isMounted = false; };
  }, [id]);

  return { order, loading, error };
}
