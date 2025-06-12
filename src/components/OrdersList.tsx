import { useEffect } from 'react';
import { useFetchOrders } from '../hooks/useFetchOrders';
import { Order } from '../types';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';

/**
 * Component for displaying a list of orders
 */
export default function OrdersList() {
  const { loading, error, orders, fetchOrders } = useFetchOrders();

  useEffect(() => {
    // Fetch orders when component mounts
    fetchOrders();
  }, []);

  // Format date string to a more readable format
  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('nl-NL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
      });
    } catch (e) {
      return dateString;
    }
  };

  // Render loading state
  if (loading) {
    return (
      <div className="flex items-center justify-center p-6">
        <div className="text-lg">Bestellingen laden...</div>
      </div>
    );
  }

  // Render error state
  if (error) {
    return (
      <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md">
        <h3 className="text-lg font-medium">Fout bij ophalen bestellingen</h3>
        <p>{error}</p>
      </div>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Bestellingen</CardTitle>
      </CardHeader>
      <CardContent>
        {orders.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Geen bestellingen gevonden.
          </div>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Order-ID</TableHead>
                <TableHead>Klant</TableHead>
                <TableHead>Product</TableHead>
                <TableHead>Datum</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {orders.map((order: Order) => (
                <TableRow key={order.id}>
                  <TableCell className="font-mono">{order.order_id}</TableCell>
                  <TableCell>{order.klant_naam || 'Onbekend'}</TableCell>
                  <TableCell>{order.product_naam}</TableCell>
                  <TableCell>{formatDate(order.bestel_datum)}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
