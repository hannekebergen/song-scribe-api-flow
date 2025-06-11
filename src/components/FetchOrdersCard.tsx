
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Download, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { wakeBackend } from '@/api/wakeBackend';
import { API } from '@/api/config';

interface FetchResult {
  new_orders: number;
  skipped_orders: number;
}

const FetchOrdersCard = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [isWakingBackend, setIsWakingBackend] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<FetchResult | null>(null);

  const handleFetchOrders = async () => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    try {
      // Wake backend before fetching orders to avoid cold-start 404
      setIsWakingBackend(true);
      try {
        await wakeBackend();
      } catch (wakeError) {
        throw new Error(`Backend wake-up mislukt: ${wakeError instanceof Error ? wakeError.message : 'Onbekende fout'}`);
      } finally {
        setIsWakingBackend(false);
      }
      
      const response = await fetch(`${API}/orders/fetch`, {
        method: 'POST',
        headers: {
          'X-API-Key': 'jouwsong2025',
          'Content-Type': 'application/json',
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      
      if (data.result) {
        setResult(data.result);
      } else {
        throw new Error('Onverwacht response format');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Er is een fout opgetreden');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="bg-white shadow-sm border rounded-lg">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Download className="h-5 w-5" />
          Orders Ophalen
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <Button 
          onClick={handleFetchOrders}
          disabled={isLoading}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-md"
        >
          {isLoading ? 'Bezig met ophalen...' : 'Haal nieuwe orders op'}
        </Button>

        {isWakingBackend && (
          <div className="flex items-center justify-center gap-2 text-center text-gray-600 p-4">
            <Loader2 className="h-4 w-4 animate-spin" />
            <span>Backend wordt opgestart (max 30s)...</span>
          </div>
        )}

        {isLoading && !isWakingBackend && (
          <div className="text-center text-gray-600 p-4">
            Bezig met ophalen...
          </div>
        )}

        {error && (
          <div className="flex items-center gap-2 p-4 bg-red-50 border border-red-200 rounded-md">
            <AlertCircle className="h-4 w-4 text-red-600" />
            <span className="text-red-700">{error}</span>
          </div>
        )}

        {result && (
          <div className="flex items-center gap-2 p-4 bg-green-50 border border-green-200 rounded-md">
            <CheckCircle className="h-4 w-4 text-green-600" />
            <div className="text-green-700">
              <div>Succesvol opgehaald!</div>
              <div className="text-sm">
                Nieuwe orders: {result.new_orders} | Overgeslagen: {result.skipped_orders}
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default FetchOrdersCard;
