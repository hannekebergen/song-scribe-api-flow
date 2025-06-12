import { useEffect, useState } from 'react';
import { useFetchOrders } from '../hooks/useFetchOrders';
import { Order } from '../types';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, AlertCircle } from 'lucide-react';

/**
 * Component for displaying a list of orders
 */
export default function OrdersList() {
  const { loading, error, orders, syncResult, fetchOrders, syncOrders } = useFetchOrders();
  const [refreshing, setRefreshing] = useState(false);
  const [syncingOrders, setSyncingOrders] = useState(false);

  useEffect(() => {
    // Fetch orders when component mounts
    fetchOrders();
  }, []);

  // Handle refresh button click - fetches existing orders from the API
  const handleRefresh = async () => {
    setRefreshing(true);
    await fetchOrders();
    setRefreshing(false);
  };
  
  // Handle sync button click - fetches new orders from the payment provider
  const handleSyncOrders = async () => {
    setSyncingOrders(true);
    await syncOrders();
    setSyncingOrders(false);
  };

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
        <Button 
          variant="outline" 
          className="mt-4" 
          onClick={handleRefresh}
          disabled={refreshing}
        >
          <Loader2 className="h-4 w-4 mr-2" />
          Probeer opnieuw
        </Button>
      </div>
    );
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Bestellingen</CardTitle>
        <div className="flex gap-2">
          <Button 
            variant="outline" 
            size="sm" 
            onClick={handleRefresh}
            disabled={refreshing || syncingOrders}
          >
            <Loader2 className={`h-4 w-4 mr-2 ${refreshing ? 'animate-spin' : ''}`} />
            {refreshing ? 'Bezig...' : 'Vernieuwen'}
          </Button>
          <Button 
            variant="default" 
            size="sm" 
            onClick={handleSyncOrders}
            disabled={refreshing || syncingOrders}
          >
            <Loader2 className={`h-4 w-4 mr-2 ${syncingOrders ? 'animate-spin' : ''}`} />
            {syncingOrders ? 'Bezig...' : 'Haal nieuwe orders op'}
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        {syncResult && (
          <div className="mb-4 p-3 bg-green-50 border border-green-200 rounded-md text-green-700">
            <p className="text-sm font-medium">Orders succesvol opgehaald!</p>
            <p className="text-xs">Nieuwe orders: {syncResult.new_orders}, Overgeslagen: {syncResult.skipped_orders}</p>
          </div>
        )}
        
        {orders.length === 0 ? (
          <div className="text-center py-8 text-muted-foreground">
            Geen bestellingen gevonden.
          </div>
        ) : (
          <>
            <div className="text-sm text-muted-foreground mb-4">
              Totaal aantal bestellingen: {orders.length}
            </div>
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
          </>
        )}
      </CardContent>
    </Card>
  );
}
