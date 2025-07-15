import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Loader2 } from 'lucide-react';
import { 
  TrashIcon, 
  CheckCircleIcon, 
  CalendarIcon, 
  FileTextIcon, 
  RotateIcon 
} from '@/components/icons/IconComponents';
import { useToast } from '@/hooks/use-toast';
import { API } from '@/api/config';

interface OrderStats {
  total_orders: number;
  recent_orders: number;
  month_orders: number;
  quarter_orders: number;
  old_orders: number;
  cleanup_candidates: number;
  stats_generated_at: string;
}

interface OldOrder {
  id: number;
  order_id: number;
  klant_naam: string;
  bestel_datum: string;
  thema: string;
  product_naam: string;
}

interface CleanupResponse {
  success: boolean;
  processed_count: number;
  failed_count: number;
  message: string;
  affected_orders?: number[];
}

const OrderCleanupManager = () => {
  const [stats, setStats] = useState<OrderStats | null>(null);
  const [oldOrders, setOldOrders] = useState<OldOrder[]>([]);
  const [loading, setLoading] = useState(false);
  const [cleanupLoading, setCleanupLoading] = useState(false);
  const [daysOld, setDaysOld] = useState(90);
  const [previewMode, setPreviewMode] = useState(true);
  const { toast } = useToast();

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/admin/orders/stats`, {
        headers: {
          'X-API-Key': 'jouwsong2025',
        },
      });
      
      if (!response.ok) throw new Error('Failed to fetch stats');
      
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error('Error fetching stats:', error);
      toast({
        title: "Fout",
        description: "Kon statistieken niet ophalen",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const fetchOldOrders = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API}/api/admin/orders/old?days_old=${daysOld}&limit=20`, {
        headers: {
          'X-API-Key': 'jouwsong2025',
        },
      });
      
      if (!response.ok) throw new Error('Failed to fetch old orders');
      
      const data = await response.json();
      setOldOrders(data.orders || []);
    } catch (error) {
      console.error('Error fetching old orders:', error);
      toast({
        title: "Fout",
        description: "Kon oude orders niet ophalen",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleCleanup = async () => {
    setCleanupLoading(true);
    try {
      const response = await fetch(`${API}/api/admin/orders/cleanup`, {
        method: 'POST',
        headers: {
          'X-API-Key': 'jouwsong2025',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          days_old: daysOld,
          dry_run: previewMode,
        }),
      });
      
      if (!response.ok) throw new Error('Cleanup failed');
      
      const result: CleanupResponse = await response.json();
      
      if (result.success) {
        toast({
          title: previewMode ? "Preview voltooid" : "Cleanup voltooid",
          description: result.message,
          duration: 5000,
        });
        
        if (!previewMode) {
          // Refresh data na echte cleanup
          await fetchStats();
          await fetchOldOrders();
        }
      } else {
        throw new Error(result.message || 'Cleanup failed');
      }
    } catch (error) {
      console.error('Error during cleanup:', error);
      toast({
        title: "Fout",
        description: `Cleanup mislukt: ${error instanceof Error ? error.message : 'Onbekende fout'}`,
        variant: "destructive",
      });
    } finally {
      setCleanupLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    fetchOldOrders();
  }, [daysOld]);

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('nl-NL', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold">Order Cleanup Manager</h2>
          <p className="text-muted-foreground">Beheer en archiveer oude orders</p>
        </div>
        <Button onClick={fetchStats} disabled={loading} variant="outline">
          <RotateIcon className={`h-4 w-4 mr-2 ${loading ? 'animate-spin' : ''}`} />
          Vernieuwen
        </Button>
      </div>

      {/* Statistics Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Totaal Orders</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stats.total_orders}</div>
              <Badge variant="outline" className="mt-1">
                Alle orders
              </Badge>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Recent (7 dagen)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-green-600">{stats.recent_orders}</div>
              <Badge variant="outline" className="mt-1">
                <CalendarIcon className="h-3 w-3 mr-1" />
                Recent
              </Badge>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Maand (7-30 dagen)</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-blue-600">{stats.month_orders}</div>
              <Badge variant="outline" className="mt-1">
                Maand
              </Badge>
            </CardContent>
          </Card>
          
          <Card>
            <CardHeader className="pb-2">
              <CardTitle className="text-sm font-medium">Cleanup Kandidaten</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold text-orange-600">{stats.cleanup_candidates}</div>
                                            <Badge variant="outline" className="mt-1">
                <span className="mr-1">⚠️</span>
                &gt; 3 maanden
              </Badge>
            </CardContent>
          </Card>
        </div>
      )}

      {/* Cleanup Controls */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <TrashIcon className="h-5 w-5" />
            Cleanup Instellingen
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2">
                Orders ouder dan (dagen)
              </label>
              <Input
                type="number"
                value={daysOld}
                onChange={(e) => setDaysOld(parseInt(e.target.value) || 90)}
                min={30}
                max={365}
                className="w-full"
              />
            </div>
            
            <div className="flex items-end">
              <Button
                onClick={() => setPreviewMode(!previewMode)}
                variant={previewMode ? "default" : "destructive"}
                className="w-full"
              >
                {previewMode ? (
                  <>
                    <span className="mr-2">ℹ️</span>
                    Preview Mode
                  </>
                ) : (
                  <>
                    <span className="mr-2">⚠️</span>
                    Deletion Mode
                  </>
                )}
              </Button>
            </div>
            
            <div className="flex items-end">
              <Button
                onClick={handleCleanup}
                disabled={cleanupLoading}
                className="w-full"
                variant={previewMode ? "outline" : "destructive"}
              >
                {cleanupLoading ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-2 animate-spin" />
                    Bezig...
                  </>
                ) : (
                  <>
                    <TrashIcon className="h-4 w-4 mr-2" />
                    {previewMode ? 'Preview Cleanup' : 'Voer Cleanup Uit'}
                  </>
                )}
              </Button>
            </div>
          </div>
          
          <Alert>
            <span className="mr-2">ℹ️</span>
            <AlertDescription>
              {previewMode ? (
                <span>Preview mode: Geen orders worden verwijderd. Schakel naar deletion mode voor echte verwijdering.</span>
              ) : (
                <span className="text-red-600">
                  <strong>Deletion mode: Orders worden definitief verwijderd!</strong> Dit kan niet ongedaan worden gemaakt.
                </span>
              )}
            </AlertDescription>
          </Alert>
        </CardContent>
      </Card>

      {/* Old Orders Preview */}
      {oldOrders.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <FileTextIcon className="h-5 w-5" />
              Oude Orders (Preview)
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              {oldOrders.map((order) => (
                <div key={order.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <div className="font-medium">
                      Order #{order.order_id} - {order.klant_naam || 'Onbekend'}
                    </div>
                    <div className="text-sm text-gray-600">
                      {formatDate(order.bestel_datum)} • {order.thema || 'Geen thema'} • {order.product_naam}
                    </div>
                  </div>
                  <Badge variant="outline" className="text-xs">
                    {order.bestel_datum ? 
                      `${Math.floor((new Date().getTime() - new Date(order.bestel_datum).getTime()) / (1000 * 60 * 60 * 24))} dagen oud` : 
                      'Onbekende datum'
                    }
                  </Badge>
                </div>
              ))}
            </div>
            
            {oldOrders.length === 20 && (
              <div className="text-center mt-4 text-sm text-gray-600">
                Eerste 20 orders getoond. Totaal: {stats?.cleanup_candidates || 0} orders
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default OrderCleanupManager; 