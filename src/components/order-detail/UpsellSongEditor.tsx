import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { 
  EditIcon, 
  SaveIcon, 
  RotateIcon, 
  CheckIcon, 
  ArrowUpIcon, 
  FileTextIcon,
  TrendingUpIcon
} from '@/components/icons/IconComponents';
import { useToast } from '@/hooks/use-toast';
import { ordersApi } from '@/services/api';
import { Order } from '@/types';

interface UpsellSongEditorProps {
  order: Order;
  onOrderUpdate: (updatedOrder: Order) => void;
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
      
      toast({
        title: "Opgeslagen",
        description: "Songtekst succesvol bijgewerkt",
      });
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

  const handleExtend = async () => {
    try {
      setExtending(true);
      const response = await ordersApi.extendSongtext(
        originalSongtext,
        extensionType,
        additionalInfo
      );
      
      if (response.success) {
        setEditedSongtext(response.extended_songtext);
        toast({
          title: "Uitgebreid",
          description: "Songtekst succesvol uitgebreid",
        });
      } else {
        throw new Error(response.error || 'Uitbreiding mislukt');
      }
    } catch (error) {
      console.error('Error extending songtext:', error);
      toast({
        title: "Fout",
        description: "Kon songtekst niet uitbreiden",
        variant: "destructive",
      });
    } finally {
      setExtending(false);
    }
  };

  const handleReset = () => {
    setEditedSongtext(originalSongtext);
  };

  const hasChanges = editedSongtext !== originalSongtext;

  if (loading) {
    return (
      <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <ArrowUpIcon className="h-5 w-5 text-purple-600" />
            Upsell Order - Songtekst Uitbreiding
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center justify-center py-8">
            <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-purple-600"></div>
            <span className="ml-2 text-gray-600">Originele songtekst laden...</span>
          </div>
        </CardContent>
      </Card>
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
                Order #{originalOrderInfo.order_id} - {originalOrderInfo.klant_naam}
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
        </CardContent>
      </Card>

      {/* AI Uitbreiding Controls */}
      <Card className="border-0 shadow-xl bg-purple-50/50 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center gap-2 text-gray-800">
            <TrendingUpIcon className="h-5 w-5 text-purple-600" />
            AI Songtekst Uitbreiding
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type Uitbreiding
              </label>
              <Select value={extensionType} onValueChange={setExtensionType}>
                <SelectTrigger>
                  <SelectValue placeholder="Selecteer uitbreiding type" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="extra_coupletten">Extra Coupletten</SelectItem>
                  <SelectItem value="bridge">Bridge</SelectItem>
                  <SelectItem value="outro">Outro</SelectItem>
                  <SelectItem value="intro">Intro</SelectItem>
                  <SelectItem value="refrein_variatie">Refrein Variatie</SelectItem>
                </SelectContent>
              </Select>
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Extra Informatie
              </label>
              <Textarea
                value={additionalInfo}
                onChange={(e) => setAdditionalInfo(e.target.value)}
                placeholder="Bijvoorbeeld: meer emotioneel, focus op herinneringen, etc."
                className="min-h-[80px]"
              />
            </div>
          </div>
          
          <Button 
            onClick={handleExtend}
            disabled={extending}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white"
          >
            <TrendingUpIcon className="h-4 w-4 mr-2" />
            {extending ? 'Uitbreiden...' : 'Songtekst Uitbreiden'}
          </Button>
        </CardContent>
      </Card>

      {/* Bewerkte Songtekst Editor */}
      <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
        <CardHeader className="pb-4">
          <CardTitle className="flex items-center justify-between text-gray-800">
            <div className="flex items-center gap-2">
              <EditIcon className="h-5 w-5 text-green-600" />
              Uitgebreide Songtekst
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
              {saving ? 'Opslaan...' : 'Opslaan'}
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
                De AI kan helpen om de songtekst uit te breiden met extra coupletten, 
                een bridge, of andere elementen die passen bij het originele thema.
              </AlertDescription>
            </Alert>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default UpsellSongEditor; 