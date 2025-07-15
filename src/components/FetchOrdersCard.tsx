
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, Loader2, CheckCircle, AlertCircle } from 'lucide-react';
import { ordersApi } from '@/services/api';
import { useToast } from '@/hooks/use-toast';

interface FetchOrdersCardProps {
  onOrdersUpdated: () => void;
}

const FetchOrdersCard = ({ onOrdersUpdated }: FetchOrdersCardProps) => {
  const [isLoading, setIsLoading] = useState(false);
  const [lastSync, setLastSync] = useState<Date | null>(null);
  const { toast } = useToast();

  const handleFetchOrders = async () => {
    setIsLoading(true);
    try {
      const result = await ordersApi.syncOrders();
      setLastSync(new Date());
      
      // Auto-refresh orders na sync
      setTimeout(() => {
        onOrdersUpdated();
      }, 1000);
      
      toast({
        title: "Orders gesynchroniseerd",
        description: `${result.new_orders} nieuwe orders toegevoegd, ${result.skipped_orders} orders overgeslagen`,
        duration: 5000,
      });
    } catch (error) {
      console.error('Error fetching orders:', error);
      toast({
        title: "Fout bij synchronisatie",
        description: "Er is een fout opgetreden bij het ophalen van orders",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="h-5 w-5" />
          Orders Synchroniseren
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <p className="text-sm text-muted-foreground">
          Haal de nieuwste orders op van Plug&Pay en werk de database bij.
        </p>
        
        {lastSync && (
          <div className="flex items-center gap-2 text-sm text-green-600">
            <CheckCircle className="h-4 w-4" />
            Laatste sync: {lastSync.toLocaleString('nl-NL')}
          </div>
        )}
        
        <Button 
          onClick={handleFetchOrders} 
          disabled={isLoading}
          className="w-full"
        >
          {isLoading ? (
            <>
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
              Bezig met synchroniseren...
            </>
          ) : (
            <>
              <Download className="mr-2 h-4 w-4" />
              Haal Orders Op
            </>
          )}
        </Button>
        
        <div className="text-xs text-muted-foreground">
          <p>• Orders worden automatisch bijgewerkt na synchronisatie</p>
          <p>• Bestaande orders worden overgeslagen</p>
          <p>• Nieuwe orders worden direct zichtbaar</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default FetchOrdersCard;
