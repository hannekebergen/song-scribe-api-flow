
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Download, AlertCircle, CheckCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { useToast } from '@/hooks/use-toast';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';

const OrderDetail = () => {
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [editedSongtext, setEditedSongtext] = useState('');
  const [saving, setSaving] = useState(false);
  const [regenerating, setRegenerating] = useState(false);

  useEffect(() => {
    if (id) {
      loadOrder(id);
    }
  }, [id]);

  useEffect(() => {
    if (order) {
      setEditedSongtext(order.songtekst);
    }
  }, [order]);

  const loadOrder = async (orderId: string) => {
    try {
      const data = await ordersApi.getOrder(Number(orderId));
      setOrder(data);
    } catch (error) {
      console.error('Error loading order:', error);
      toast({
        title: "Fout",
        description: "Kon order niet laden",
        variant: "destructive",
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    if (!order) return;

    setSaving(true);
    try {
      const updatedOrder = await ordersApi.updateSongtext(String(order.order_id), editedSongtext);
      if (updatedOrder) {
        setOrder(updatedOrder);
        toast({
          title: "Opgeslagen",
          description: "Songtekst succesvol bijgewerkt",
        });
      }
    } catch (error) {
      console.error('Error saving songtext:', error);
      toast({
        title: "Fout",
        description: "Kon songtekst niet opslaan",
        variant: "destructive",
      });
    } finally {
      setSaving(false);
    }
  };

  const handleRegenerate = async () => {
    if (!order) return;

    setRegenerating(true);
    try {
      const updatedOrder = await ordersApi.regeneratePrompt(String(order.order_id));
      if (updatedOrder) {
        setOrder(updatedOrder);
        setEditedSongtext(updatedOrder.songtekst);
        toast({
          title: "Hergenereerd",
          description: "Nieuwe songtekst gegenereerd",
        });
      }
    } catch (error) {
      console.error('Error regenerating prompt:', error);
      toast({
        title: "Fout",
        description: "Kon prompt niet hergenereren",
        variant: "destructive",
      });
    } finally {
      setRegenerating(false);
    }
  };

  const handleDownload = async (type: 'json' | 'txt') => {
    if (!order) return;

    try {
      const data = await ordersApi.downloadOrder(String(order.order_id), type);
      const blob = new Blob([data], { 
        type: type === 'json' ? 'application/json' : 'text/plain' 
      });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `order-${String(order.order_id)}.${type}`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);

      toast({
        title: "Download gestart",
        description: `Bestand wordt gedownload als ${type.toUpperCase()}`,
      });
    } catch (error) {
      console.error('Error downloading:', error);
      toast({
        title: "Fout",
        description: "Download mislukt",
        variant: "destructive",
      });
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Order laden...</div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="container mx-auto p-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold mb-4">Order niet gevonden</h1>
          <Button asChild>
            <Link to="/dashboard">
              <Download className="h-4 w-4 mr-2" />
              Terug naar dashboard
            </Link>
          </Button>
        </div>
      </div>
    );
  }

  const hasChanges = editedSongtext !== order.songtekst;

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <Button asChild variant="outline">
          <Link to="/dashboard">
            <Download className="h-4 w-4 mr-2" />
            Terug naar dashboard
          </Link>
        </Button>
        
        <div className="flex gap-2">
          <Button 
            onClick={() => handleDownload('json')}
            variant="outline"
            size="sm"
          >
            <AlertCircle className="h-4 w-4 mr-2" />
            Download JSON
          </Button>
          <Button 
            onClick={() => handleDownload('txt')}
            variant="outline" 
            size="sm"
          >
            <CheckCircle className="h-4 w-4 mr-2" />
            Download TXT
          </Button>
          <Button 
            onClick={handleRegenerate}
            disabled={regenerating}
            size="sm"
          >
            <Loader2 className={`h-4 w-4 mr-2 ${regenerating ? 'animate-spin' : ''}`} />
            Hergenereer
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Order #{order.order_id}
                <Badge variant={order.status === 'nieuw' ? 'outline' : 'default'}>
                  {order.status === 'nieuw' ? 'Nieuw' : 'Gegenereerd'}
                </Badge>
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Voornaam</label>
                  <div className="font-medium">{order.voornaam}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Van</label>
                  <div className="font-medium">{order.van_naam}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Relatie</label>
                  <div className="font-medium">{order.relatie}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Datum</label>
                  <div className="font-medium">{new Date(order.datum).toLocaleDateString('nl-NL')}</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Thema & Stijl</CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Thema</label>
                  <div className="font-medium">{order.thema}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Toon</label>
                  <div className="font-medium">{order.toon}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Structuur</label>
                  <div className="font-medium">{order.structuur}</div>
                </div>
                <div>
                  <label className="text-sm font-medium text-muted-foreground">Rijm</label>
                  <div className="font-medium">{order.rijm}</div>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Beschrijving</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm leading-relaxed">{order.beschrijving}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Persoonlijk verhaal</CardTitle>
            </CardHeader>
            <CardContent>
              <pre className="text-sm leading-relaxed bg-gray-50 p-3 rounded whitespace-pre-wrap">
                {order.raw_data?.address?.note ? order.raw_data.address.note : "Geen persoonlijk verhaal meegegeven."}
              </pre>
            </CardContent>
          </Card>
        </div>

        <div className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center justify-between">
                Songtekst Editor
                {hasChanges && (
                  <Badge variant="outline">Niet opgeslagen wijzigingen</Badge>
                )}
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <Textarea
                value={editedSongtext}
                onChange={(e) => setEditedSongtext(e.target.value)}
                placeholder="Songtekst..."
                className="min-h-[400px] font-mono text-sm"
              />
              
              <div className="flex gap-2">
                <Button 
                  onClick={handleSave}
                  disabled={!hasChanges || saving}
                  className="flex-1"
                >
                  <CheckCircle className="h-4 w-4 mr-2" />
                  {saving ? 'Opslaan...' : 'Opslaan'}
                </Button>
                
                {hasChanges && (
                  <Button 
                    variant="outline"
                    onClick={() => setEditedSongtext(order.songtekst)}
                  >
                    Reset
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;
