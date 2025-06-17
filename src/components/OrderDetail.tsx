
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Download, AlertCircle, CheckCircle, Loader2, ArrowLeft, FileText, Edit3, Save, RotateCcw, Calendar, User, Heart, Music } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
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
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex items-center justify-center">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <div className="text-lg font-medium text-gray-700">Order laden...</div>
        </div>
      </div>
    );
  }

  if (!order) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
        <div className="container mx-auto p-6">
          <div className="text-center py-20">
            <div className="mb-6">
              <AlertCircle className="h-16 w-16 mx-auto text-gray-400" />
            </div>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Order niet gevonden</h1>
            <p className="text-gray-600 mb-8">De opgevraagde order bestaat niet of is niet toegankelijk.</p>
            <Button asChild className="bg-blue-600 hover:bg-blue-700">
              <Link to="/dashboard">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Terug naar dashboard
              </Link>
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const hasChanges = editedSongtext !== order.songtekst;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <Button asChild variant="outline" className="border-gray-200 hover:bg-white">
              <Link to="/dashboard">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Terug naar dashboard
              </Link>
            </Button>
            
            <div className="space-y-1">
              <h1 className="text-3xl font-bold text-gray-800">
                Order #{order.order_id}
              </h1>
              <div className="flex items-center space-x-2">
                <Badge variant={order.status === 'nieuw' ? 'outline' : 'default'} className="font-medium">
                  {order.status === 'nieuw' ? 'Nieuw' : 'Gegenereerd'}
                </Badge>
                {hasChanges && (
                  <Badge variant="outline" className="text-orange-600 border-orange-200 bg-orange-50">
                    Niet opgeslagen wijzigingen
                  </Badge>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex flex-wrap gap-2">
            <Button 
              onClick={() => handleDownload('json')}
              variant="outline"
              size="sm"
              className="border-gray-200 hover:bg-gray-50"
            >
              <FileText className="h-4 w-4 mr-2" />
              Download JSON
            </Button>
            <Button 
              onClick={() => handleDownload('txt')}
              variant="outline" 
              size="sm"
              className="border-gray-200 hover:bg-gray-50"
            >
              <Download className="h-4 w-4 mr-2" />
              Download TXT
            </Button>
            <Button 
              onClick={handleRegenerate}
              disabled={regenerating}
              size="sm"
              className="bg-blue-600 hover:bg-blue-700"
            >
              <Loader2 className={`h-4 w-4 mr-2 ${regenerating ? 'animate-spin' : ''}`} />
              Hergenereer
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Left Column - Order Details */}
          <div className="space-y-6">
            {/* Basic Info */}
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <User className="h-5 w-5 text-blue-600" />
                  Persoonlijke Gegevens
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Voornaam</label>
                    <div className="text-lg font-medium text-gray-800">{order.voornaam}</div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Van</label>
                    <div className="text-lg font-medium text-gray-800">{order.van_naam}</div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Relatie</label>
                    <div className="text-lg font-medium text-gray-800">{order.relatie}</div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Datum</label>
                    <div className="flex items-center gap-2 text-lg font-medium text-gray-800">
                      <Calendar className="h-4 w-4 text-blue-600" />
                      {new Date(order.datum).toLocaleDateString('nl-NL', {
                        weekday: 'long',
                        year: 'numeric',
                        month: 'long',
                        day: 'numeric'
                      })}
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Song Details */}
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <Music className="h-5 w-5 text-blue-600" />
                  Song Specificaties
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Thema</label>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-800 font-medium text-base px-3 py-1">
                      {order.thema}
                    </Badge>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Toon</label>
                    <div className="text-lg font-medium text-gray-800">{order.toon}</div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Structuur</label>
                    <div className="text-lg font-medium text-gray-800">{order.structuur}</div>
                  </div>
                  <div className="space-y-1">
                    <label className="text-sm font-semibold text-gray-600">Rijm</label>
                    <div className="text-lg font-medium text-gray-800">{order.rijm}</div>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Description */}
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <Heart className="h-5 w-5 text-red-500" />
                  Beschrijving
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">{order.beschrijving}</p>
                </div>
              </CardContent>
            </Card>

            {/* Personal Story */}
            <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <FileText className="h-5 w-5 text-green-600" />
                  Persoonlijk verhaal
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="bg-green-50 p-4 rounded-lg border border-green-200">
                  <pre className="text-gray-700 leading-relaxed whitespace-pre-wrap font-sans">
                    {order.raw_data?.address?.note ? order.raw_data.address.note : "Geen persoonlijk verhaal meegegeven."}
                  </pre>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column - Song Editor */}
          <div className="space-y-6">
            <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center justify-between text-gray-800">
                  <div className="flex items-center gap-2">
                    <Edit3 className="h-5 w-5 text-purple-600" />
                    Songtekst Editor
                  </div>
                  {hasChanges && (
                    <Badge variant="outline" className="text-orange-600 border-orange-200 bg-orange-50 animate-pulse">
                      Niet opgeslagen
                    </Badge>
                  )}
                </CardTitle>
                <Separator />
              </CardHeader>
              <CardContent className="space-y-6">
                <Textarea
                  value={editedSongtext}
                  onChange={(e) => setEditedSongtext(e.target.value)}
                  placeholder="Songtekst..."
                  className="min-h-[500px] font-mono text-sm leading-relaxed border-gray-200 focus:border-purple-500 focus:ring-purple-500 resize-none"
                />
                
                <div className="flex flex-col sm:flex-row gap-3">
                  <Button 
                    onClick={handleSave}
                    disabled={!hasChanges || saving}
                    className="flex-1 bg-green-600 hover:bg-green-700 text-white"
                  >
                    <Save className="h-4 w-4 mr-2" />
                    {saving ? 'Opslaan...' : 'Opslaan'}
                  </Button>
                  
                  {hasChanges && (
                    <Button 
                      variant="outline"
                      onClick={() => setEditedSongtext(order.songtekst)}
                      className="border-gray-200 hover:bg-gray-50"
                    >
                      <RotateCcw className="h-4 w-4 mr-2" />
                      Reset
                    </Button>
                  )}
                </div>

                {order.songtekst && order.songtekst.length > 0 && (
                  <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                    <div className="flex items-center gap-2 mb-2">
                      <CheckCircle className="h-4 w-4 text-blue-600" />
                      <span className="text-sm font-medium text-blue-800">
                        Status: Songtekst beschikbaar
                      </span>
                    </div>
                    <p className="text-sm text-blue-700">
                      De songtekst is {order.songtekst.split('\n').length} regels lang en bevat {order.songtekst.length} karakters.
                    </p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;
