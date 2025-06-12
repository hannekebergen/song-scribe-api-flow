import { useEffect, useState } from 'react';
import { useFetchOrders, MappedOrder } from '../hooks/useFetchOrders';
import { useOrder } from '../hooks/useOrder';
import { Order } from '../types';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Loader2, AlertCircle } from 'lucide-react';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';

// Order Detail Modal Component
interface OrderDetailModalProps {
  isOpen: boolean;
  onClose: () => void;
  orderId: number | null;
}

function OrderDetailModal({ isOpen, onClose, orderId }: OrderDetailModalProps) {
  // Only fetch order data if modal is open and we have an orderId
  const { order, loading, error } = useOrder(orderId || 0);
  
  // Format date for display
  const formatDate = (dateString: string) => {
    try {
      return new Date(dateString).toLocaleDateString('nl-NL', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch (e) {
      return dateString;
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent className="sm:max-w-md">
        <DialogHeader>
          <DialogTitle>Order Details</DialogTitle>
          <DialogDescription>
            Bekijk de details van deze bestelling
          </DialogDescription>
        </DialogHeader>
        
        {loading && (
          <div className="flex items-center justify-center p-6">
            <Loader2 className="h-6 w-6 animate-spin mr-2" />
            <span>Gegevens laden...</span>
          </div>
        )}
        
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-md">
            <h3 className="text-lg font-medium">Fout bij ophalen bestelling</h3>
            <p>{error}</p>
          </div>
        )}
        
        {!loading && !error && order && (
          <div className="grid gap-4">
            <div className="grid grid-cols-2 gap-2">
              <div className="font-medium">Order ID:</div>
              <div className="font-mono">{order.order_id}</div>
              
              <div className="font-medium">Klant:</div>
              <div>{order.klant_naam || 'Onbekend'}</div>
              
              <div className="font-medium">Email:</div>
              <div>{order.klant_email || 'Onbekend'}</div>
              
              <div className="font-medium">Product:</div>
              <div>{order.product_naam}</div>
              
              <div className="font-medium">Datum:</div>
              <div>{formatDate(order.bestel_datum)}</div>
            </div>
            
            <div className="flex justify-end">
              <Button variant="outline" onClick={onClose}>Sluiten</Button>
            </div>
          </div>
        )}
      </DialogContent>
    </Dialog>
  );
}

/**
 * Component for displaying a list of orders
 */
export default function OrdersList() {
  const { loading, error, orders, mappedOrders, syncResult, fetchOrders, syncOrders } = useFetchOrders();
  const [refreshing, setRefreshing] = useState(false);
  const [syncingOrders, setSyncingOrders] = useState(false);
  const [selectedOrderId, setSelectedOrderId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

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
    <>
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
                Totaal aantal bestellingen: {mappedOrders.length}
              </div>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Ordernummer</TableHead>
                    <TableHead>Datum</TableHead>
                    <TableHead>Thema</TableHead>
                    <TableHead>Klant</TableHead>
                    <TableHead>Deadline</TableHead>
                    <TableHead>Actie</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {mappedOrders.map((row: MappedOrder) => (
                    <TableRow key={row.originalOrder.id}>
                      <TableCell className="font-mono">{row.ordernummer}</TableCell>
                      <TableCell>{row.datum}</TableCell>
                      <TableCell>{row.thema}</TableCell>
                      <TableCell>{row.klant}</TableCell>
                      <TableCell>{row.deadline}</TableCell>
                      <TableCell>
                        <Button 
                          variant="ghost" 
                          size="sm"
                          onClick={() => {
                            setSelectedOrderId(row.originalOrder.id);
                            setIsModalOpen(true);
                          }}
                        >
                          Bekijk
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </>
          )}
        </CardContent>
      </Card>

      {/* Order Detail Modal */}
      <OrderDetailModal 
        isOpen={isModalOpen} 
        onClose={() => setIsModalOpen(false)} 
        orderId={selectedOrderId} 
      />
    </>
  );
}
