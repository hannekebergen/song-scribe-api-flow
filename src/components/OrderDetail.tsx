import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';
import { XIcon, ArrowLeftIcon, FileTextIcon, ArrowUpIcon } from '@/components/icons/IconComponents';
import PersonalInfoCard from './order-detail/PersonalInfoCard';
import DescriptionCard from './order-detail/DescriptionCard';
import SongEditor from './order-detail/SongEditor';
import AIPromptCard from './order-detail/AIPromptCard';
import { detectOrderType } from '@/utils/orderTypeDetection';
import UpsellSongEditor from './order-detail/UpsellSongEditor';
import { SunoMusicCard } from './order-detail/SunoMusicCard';

const OrderDetail = () => {
  const { id } = useParams<{ id: string }>();
  const { toast } = useToast();
  const [order, setOrder] = useState<Order | null>(null);
  const [loading, setLoading] = useState(true);
  const [editedSongtext, setEditedSongtext] = useState('');
  const [saving, setSaving] = useState(false);
  const [regenerating, setRegenerating] = useState(false);
  const songtextRef = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (id) {
      loadOrder(id);
    }
  }, [id]);

  useEffect(() => {
    if (order) {
      setEditedSongtext(order.songtekst || '');
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

  // Helper functions for getting dashboard-compatible data
  const getOrderTypeDisplay = (order: Order): string => {
    // Eerst proberen backend typeOrder
    if (order.typeOrder && order.typeOrder !== 'Onbekend') {
      return order.typeOrder;
    }
    
    // Fallback naar frontend detectie (zoals in dashboard)
    const detectedType = detectOrderType(order);
    return detectedType.type;
  };

  const getKlantNaam = (order: Order): string => {
    return order.raw_data?.address?.full_name || 
      (order.raw_data?.address?.firstname && order.raw_data?.address?.lastname ? 
        `${order.raw_data.address.firstname} ${order.raw_data.address.lastname}` : 
        order.klant_naam || '-');
  };

  const handleSave = async () => {
    if (!order) return;

    setSaving(true);
    try {
      const updatedOrder = await ordersApi.updateSongtext(order.order_id, editedSongtext);
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
        setEditedSongtext(updatedOrder.songtekst || '');
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

  const handleCopyToSongtext = (prompt: string) => {
    setEditedSongtext(prompt);
    
    // Focus on the songtext editor after a brief delay
    setTimeout(() => {
      if (songtextRef.current) {
        songtextRef.current.focus();
        songtextRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }, 100);

    toast({
      title: "Gekopieerd",
      description: "Prompt is gekopieerd naar de songtekst editor",
    });
  };

  // Helper function to check if this is an upsell order
  const isUpsellOrder = (order: Order): boolean => {
    const orderType = detectOrderType(order);
    return orderType.badge === 'upsell';
  };

  // Helper function to check if upsell order has origin_song_id
  const hasOriginSongId = (order: Order): boolean => {
    return order.origin_song_id !== null && order.origin_song_id !== undefined;
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
              <XIcon className="h-16 w-16 mx-auto text-gray-400" />
            </div>
            <h1 className="text-2xl font-bold mb-4 text-gray-800">Order niet gevonden</h1>
            <p className="text-gray-600 mb-8">De opgevraagde order bestaat niet of is niet toegankelijk.</p>
            <Button asChild className="bg-blue-600 hover:bg-blue-700">
              <Link to="/dashboard">
                <ArrowLeftIcon className="h-4 w-4 mr-2" />
                Terug naar dashboard
              </Link>
            </Button>
          </div>
        </div>
      </div>
    );
  }

  const hasChanges = editedSongtext !== (order.songtekst || '');

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 p-6">
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button asChild variant="ghost" size="sm">
              <Link to="/">
                <ArrowLeftIcon className="h-4 w-4 mr-2" />
                Terug naar Dashboard
              </Link>
            </Button>
            <div className="text-sm text-gray-500">
              Order #{order.order_id} • {new Date(order.bestel_datum).toLocaleDateString('nl-NL')}
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <Badge variant="outline" className="bg-blue-100 text-blue-800">
              {getOrderTypeDisplay(order)}
            </Badge>
            <Button onClick={() => handleDownload('json')} variant="outline" size="sm">
              <FileTextIcon className="h-4 w-4 mr-2" />
              JSON
            </Button>
            <Button onClick={() => handleDownload('txt')} variant="outline" size="sm">
              <FileTextIcon className="h-4 w-4 mr-2" />
              TXT
            </Button>
            <Button onClick={() => window.location.reload()} variant="outline" size="sm">
              <XIcon className="h-4 w-4" />
            </Button>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">
          {/* Left Column - Order Info */}
          <div className="space-y-6">
            <PersonalInfoCard order={order} />
            
            {/* Conditional rendering based on order type */}
            {!isUpsellOrder(order) && (
              <DescriptionCard order={order} />
            )}
            
            {isUpsellOrder(order) && (
              <Card className="border-0 shadow-xl bg-gradient-to-br from-purple-50 to-purple-100">
                <CardHeader className="pb-4">
                  <CardTitle className="flex items-center gap-2 text-purple-800">
                    <ArrowUpIcon className="h-5 w-5" />
                    Upsell Order
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-3">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-purple-700">Originele Order:</span>
                      <Badge variant="outline" className="text-purple-600">
                        #{order.origin_song_id}
                      </Badge>
                    </div>
                    <div className="text-sm text-purple-600">
                      Deze order bouwt voort op een bestaande songtekst. 
                      Gebruik de AI uitbreiding om extra coupletten, 
                      een bridge of andere elementen toe te voegen.
                    </div>
                  </div>
                </CardContent>
              </Card>
            )}
          </div>

          {/* Right Column - Song Content */}
          <div className="xl:col-span-2 space-y-6">
            {/* Conditional rendering for different order types */}
            {!isUpsellOrder(order) && (
              <>
                <AIPromptCard 
                  order={order} 
                  onCopyToSongtext={handleCopyToSongtext}
                />
                <SongEditor
                  ref={songtextRef}
                  editedSongtext={editedSongtext}
                  setEditedSongtext={setEditedSongtext}
                  hasChanges={hasChanges}
                  saving={saving}
                  originalSongtext={order.songtekst || ''}
                  onSave={handleSave}
                  onReset={() => setEditedSongtext(order.songtekst || '')}
                />
                
                {/* Suno Music Generation Card */}
                <SunoMusicCard order={order} />
              </>
            )}

            {isUpsellOrder(order) && (
              <>
                {hasOriginSongId(order) ? (
                  <>
                    <UpsellSongEditor 
                      order={order} 
                      onOrderUpdate={setOrder}
                    />
                    
                    {/* Suno Music Generation Card for Upsell */}
                    <SunoMusicCard order={order} />
                  </>
                ) : (
                  <Card className="bg-amber-50 border-amber-200">
                    <CardContent className="p-6">
                      <div className="flex items-center gap-3 mb-4">
                        <div className="h-10 w-10 rounded-full bg-amber-100 flex items-center justify-center">
                          <span className="text-amber-600 font-semibold">!</span>
                        </div>
                        <div>
                          <h3 className="font-semibold text-amber-800">Upsell Order Niet Gelinkt</h3>
                          <p className="text-sm text-amber-700">
                            Deze upsell order is nog niet gelinkt aan een originele order.
                          </p>
                        </div>
                      </div>
                      <div className="space-y-3">
                        <p className="text-sm text-amber-700">
                          Om de originele songtekst te kunnen bewerken, moet deze upsell order eerst worden gelinkt aan de originele order.
                        </p>
                        <div className="bg-amber-100 p-3 rounded-lg">
                          <p className="text-xs text-amber-800 font-medium">
                            Voer het upsell linking proces uit via: <br />
                            <code className="bg-amber-200 px-1 rounded">POST /orders/link-upsell-orders</code>
                          </p>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;
