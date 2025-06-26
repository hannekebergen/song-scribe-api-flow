import React, { useState, useEffect, useRef } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';
import { XIcon, ArrowLeftIcon, FileTextIcon } from '@/components/icons/IconComponents';
import PersonalInfoCard from './order-detail/PersonalInfoCard';
import DescriptionCard from './order-detail/DescriptionCard';
import SongEditor from './order-detail/SongEditor';
import AIPromptCard from './order-detail/AIPromptCard';
import { detectOrderType } from '@/utils/orderTypeDetection';

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
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Header */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-4">
            <Button asChild variant="outline" className="border-gray-200 hover:bg-white">
              <Link to="/dashboard">
                <ArrowLeftIcon className="h-4 w-4 mr-2" />
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
              <FileTextIcon className="h-4 w-4 mr-2" />
              Download JSON
            </Button>
            <Button 
              onClick={() => handleDownload('txt')}
              variant="outline" 
              size="sm"
              className="border-gray-200 hover:bg-gray-50"
            >
              <FileTextIcon className="h-4 w-4 mr-2" />
              Download TXT
            </Button>
            <Button 
              onClick={handleRegenerate}
              disabled={regenerating}
              size="sm"
              className="bg-blue-600 hover:bg-blue-700"
            >
              <XIcon className={`h-4 w-4 mr-2 ${regenerating ? 'animate-spin' : ''}`} />
              Hergenereer
            </Button>
          </div>
        </div>

        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {/* Left Column - Order Details */}
          <div className="space-y-6">
            {/* Persoonlijke Gegevens - Nu eerst */}
            <PersonalInfoCard order={order} klantNaam={getKlantNaam(order)} />

            {/* Order Informatie - Nu tweede */}
            <Card className="border-0 shadow-lg bg-white/95 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="text-lg font-semibold text-gray-800 flex items-center">
                  <FileTextIcon className="h-5 w-5 mr-2 text-blue-600" />
                  Order Informatie
                </CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-sm font-medium text-gray-500">Order Type</p>
                    <p className="text-sm text-gray-900">{getOrderTypeDisplay(order)}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Thema</p>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-800">
                      {order.thema || '-'}
                    </Badge>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Toon</p>
                    <p className="text-sm text-gray-900">{order.toon || '-'}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Structuur</p>
                    <p className="text-sm text-gray-900">{order.structuur || '-'}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Deadline</p>
                    <p className="text-sm text-gray-900">{order.deadline || '-'}</p>
                  </div>
                  <div>
                    <p className="text-sm font-medium text-gray-500">Rijm</p>
                    <p className="text-sm text-gray-900">{order.rijm || '-'}</p>
                  </div>
                </div>
              </CardContent>
            </Card>

            <DescriptionCard order={order} />
          </div>

          {/* Right Column - AI Prompt and Song Editor */}
          <div className="space-y-6">
            <AIPromptCard order={order} onCopyToSongtext={handleCopyToSongtext} />
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
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderDetail;
