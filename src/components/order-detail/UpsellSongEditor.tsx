import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  FileTextIcon, 
  SaveIcon, 
  RotateIcon, 
  CheckIcon,
  SyncIcon,
  AlertTriangleIcon
} from '@/components/icons/IconComponents';
import { useToast } from '@/hooks/use-toast';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';

interface UpsellSongEditorProps {
  order: Order;
  onOrderUpdate: (order: Order) => void;
}

const UpsellSongEditor: React.FC<UpsellSongEditorProps> = ({ order, onOrderUpdate }) => {
  const [originalSongtext, setOriginalSongtext] = useState<string>('');
  const [editedSongtext, setEditedSongtext] = useState<string>('');
  const [extensionType, setExtensionType] = useState<string>('extra_coupletten');
  const [additionalInfo, setAdditionalInfo] = useState<string>('');
  const [originalOrderInfo, setOriginalOrderInfo] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [saving, setSaving] = useState<boolean>(false);
  const [extending, setExtending] = useState<boolean>(false);
  const [syncStatus, setSyncStatus] = useState<'idle' | 'syncing' | 'synced' | 'error'>('idle');
  const { toast } = useToast();

  useEffect(() => {
    loadOriginalSongtext();
  }, [order.id]);

  useEffect(() => {
    if (order.songtekst) {
      setEditedSongtext(order.songtekst);
    }
  }, [order.songtekst]);

  const loadOriginalSongtext = async () => {
    try {
      setLoading(true);
      const response: any = await ordersApi.getOriginalSongtext(order.order_id);
      
      if (response.success) {
        setOriginalSongtext(response.original_songtext || '');
        setOriginalOrderInfo(response.original_order_info || null);
        
        // Als er nog geen bewerkte songtekst is, begin met de originele
        if (!order.songtekst) {
          setEditedSongtext(response.original_songtext || '');
        }
        
        // Check of de songtekst gesynchroniseerd is
        if (response.original_songtext && order.songtekst === response.original_songtext) {
          setSyncStatus('synced');
        }
      } else {
        toast({
          title: "Waarschuwing",
          description: "Originele songtekst niet gevonden",
          variant: "destructive",
        });
      }
    } catch (error: any) {
      console.error('Error loading original songtext:', error);
      
      // Specifieke foutafhandeling voor 400 errors (order niet gelinkt)
      if (error.response?.status === 400) {
        toast({
          title: "Order niet gelinkt",
          description: "Deze upsell order is nog niet gelinkt aan een originele order. Voer eerst het linking proces uit.",
          variant: "destructive",
        });
      } else {
        toast({
          title: "Fout",
          description: "Kon originele songtekst niet laden",
          variant: "destructive",
        });
      }
    } finally {
      setLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      setSaving(true);
      const updatedOrder = await ordersApi.updateSongtext(order.order_id, editedSongtext);
      onOrderUpdate(updatedOrder);
      
      // Check of de songtekst is gesynchroniseerd
      if (originalSongtext && editedSongtext === originalSongtext) {
        setSyncStatus('synced');
        toast({
          title: "Opgeslagen & Gesynchroniseerd",
          description: "Songtekst opgeslagen en automatisch gesynchroniseerd naar UpSell orders",
        });
      } else {
        setSyncStatus('synced');
        toast({
          title: "Opgeslagen",
          description: "Songtekst succesvol bijgewerkt",
        });
      }
    } catch (error) {
      console.error('Error saving songtext:', error);
      setSyncStatus('error');
      toast({
        title: "Fout",
        description: "Kon songtekst niet opslaan",
        variant: "destructive",
      });
    } finally {
      setSaving(false);
    }
  };

  const handleSyncFromOriginal = async () => {
    try {
      setSyncStatus('syncing');
      const updatedOrder = await ordersApi.updateSongtext(order.order_id, originalSongtext);
      setEditedSongtext(originalSongtext);
      onOrderUpdate(updatedOrder);
      setSyncStatus('synced');
      
      toast({
        title: "Gesynchroniseerd",
        description: "Songtekst gesynchroniseerd van originele order",
      });
    } catch (error) {
      console.error('Error syncing from original:', error);
      setSyncStatus('error');
      toast({
        title: "Fout",
        description: "Kon niet synchroniseren van originele order",
        variant: "destructive",
      });
    }
  };

  const handleReset = () => {
    setEditedSongtext(originalSongtext);
  };

  const hasChanges = editedSongtext !== (order.songtekst || '');

  if (loading) {
    return (
      <div className="flex items-center justify-center p-8">
        <div className="text-center">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>
          <p className="text-gray-600">Originele songtekst laden...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Originele Songtekst Card */}
      <Card className="border-0 shadow-xl bg-blue-50/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <FileTextIcon className="h-5 w-5 text-blue-600" />
            Originele Songtekst
            {originalOrderInfo && (
              <Badge variant="outline" className="ml-2 text-xs">
                Order #{originalOrderInfo.original_order_id} - {originalOrderInfo.klant_naam}
              </Badge>
            )}
            {syncStatus === 'synced' && (
              <Badge variant="default" className="ml-2 text-xs bg-green-100 text-green-800">
                <SyncIcon className="h-3 w-3 mr-1" />
                Gesynchroniseerd
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-white p-4 rounded-lg border border-blue-200">
            <pre className="whitespace-pre-wrap text-sm text-gray-700 font-mono">
              {originalSongtext || 'Geen originele songtekst beschikbaar'}
            </pre>
          </div>
          
          {originalSongtext && (
            <div className="mt-4 flex gap-2">
              <Button 
                onClick={handleSyncFromOriginal}
                disabled={syncStatus === 'syncing'}
                variant="outline" 
                size="sm"
                className="border-blue-200 text-blue-600 hover:bg-blue-50"
              >
                <SyncIcon className={`h-4 w-4 mr-2 ${syncStatus === 'syncing' ? 'animate-spin' : ''}`} />
                {syncStatus === 'syncing' ? 'Synchroniseren...' : 'Synchroniseer van Origineel'}
              </Button>
              
              {syncStatus === 'synced' && (
                <Badge variant="outline" className="bg-green-50 text-green-700 border-green-200">
                  <CheckIcon className="h-3 w-3 mr-1" />
                  Up-to-date
                </Badge>
              )}
            </div>
          )}
        </CardContent>
      </Card>

      {/* AI Uitbreiding Controls */}
      <Card className="border-0 shadow-xl bg-purple-50/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <AlertTriangleIcon className="h-5 w-5 text-purple-600" />
            AI Uitbreiding
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type Uitbreiding
              </label>
              <select
                value={extensionType}
                onChange={(e) => setExtensionType(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              >
                <option value="extra_coupletten">Extra Coupletten</option>
                <option value="bridge">Bridge</option>
                <option value="outro">Outro</option>
                <option value="intro">Intro</option>
                <option value="refrein_uitbreiding">Refrein Uitbreiding</option>
              </select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Extra Informatie
              </label>
              <input
                type="text"
                value={additionalInfo}
                onChange={(e) => setAdditionalInfo(e.target.value)}
                placeholder="Bijv. 'meer emotioneel', 'vrolijker'..."
                className="w-full p-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-purple-500 focus:border-purple-500"
              />
            </div>
          </div>
          
          <Button 
            onClick={() => {/* AI uitbreiding logica */}}
            disabled={extending || !originalSongtext}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white"
          >
            <AlertTriangleIcon className="h-4 w-4 mr-2" />
            {extending ? 'AI Uitbreiding...' : 'Genereer AI Uitbreiding'}
          </Button>
        </CardContent>
      </Card>

      {/* Songtekst Editor */}
      <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <FileTextIcon className="h-5 w-5 text-green-600" />
            Uitgebreide Songtekst
            {hasChanges && (
              <Badge variant="outline" className="ml-2 text-xs bg-orange-50 text-orange-700 border-orange-200">
                Niet opgeslagen
              </Badge>
            )}
          </CardTitle>
        </CardHeader>
        
        <CardContent className="space-y-6">
          <Textarea
            value={editedSongtext}
            onChange={(e) => setEditedSongtext(e.target.value)}
            placeholder="Uitgebreide songtekst..."
            className="min-h-[500px] font-mono text-sm leading-relaxed border-gray-200 focus:border-green-500 focus:ring-green-500 resize-none"
          />
          
          <div className="flex flex-col sm:flex-row gap-3">
            <Button 
              onClick={handleSave}
              disabled={!hasChanges || saving}
              className="flex-1 bg-green-600 hover:bg-green-700 text-white"
            >
              <SaveIcon className="h-4 w-4 mr-2" />
              {saving ? 'Opslaan...' : 'Opslaan & Synchroniseren'}
            </Button>
            
            {hasChanges && (
              <Button 
                variant="outline"
                onClick={handleReset}
                className="border-gray-200 hover:bg-gray-50"
              >
                <RotateIcon className="h-4 w-4 mr-2" />
                Reset naar Origineel
              </Button>
            )}
          </div>

          {originalSongtext && (
            <Alert>
              <CheckIcon className="h-4 w-4" />
              <AlertDescription>
                <strong>Tip:</strong> Deze upsell order is gelinkt aan de originele order. 
                Wanneer je de songtekst opslaat, wordt deze automatisch gesynchroniseerd naar alle 
                gerelateerde UpSell orders die nog geen eigen songtekst hebben.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default UpsellSongEditor; 