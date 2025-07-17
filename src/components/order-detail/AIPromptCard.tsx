
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FileTextIcon, CheckIcon } from '@/components/icons/IconComponents';
import { 
  aiApi, 
  generateSongtextFromOrder, 
  generateProfessionalSongtextFromDescription,
  generateSongtextFromDescription,
  type AIProvider 
} from '@/services/aiApi';
import { themaApi, type Thema } from '@/services/themaApi';
import { Order } from '@/types';

interface AIPromptCardProps {
  order: Order;
  onCopyToSongtext: (songtext: string) => void;
}

const AIPromptCard: React.FC<AIPromptCardProps> = ({ order, onCopyToSongtext }) => {
  const [prompt, setPrompt] = useState('');
  const [songtext, setSongtext] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isGenerated, setIsGenerated] = useState(false);
  const [providers, setProviders] = useState<AIProvider[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<string>('');
  const [themas, setThemas] = useState<Thema[]>([]);
  const [selectedThemaId, setSelectedThemaId] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'prompt' | 'songtext'>('prompt');

  // Load providers and themas on component mount
  useEffect(() => {
    const loadData = async () => {
      try {
        // Load AI providers
        const providersData = await aiApi.getProviders();
        setProviders(providersData.providers);
        setSelectedProvider(providersData.default_provider);

        // Load themas
        const themasData = await themaApi.getThemas({ active_only: true });
        setThemas(themasData);
        
        // Set default thema if order has thema_id
        if (order.thema_id) {
          setSelectedThemaId(order.thema_id.toString());
        }
      } catch (err) {
        console.error('Failed to load data:', err);
        setError('Kon data niet laden');
      }
    };
    
    loadData();
  }, [order.thema_id]);

  const generatePromptFromOrder = async () => {
    if (!order.beschrijving) {
      setError('Geen beschrijving beschikbaar in de order');
      return;
    }

    try {
      // Gebruik altijd professionele prompt endpoint
      const themaId = selectedThemaId ? parseInt(selectedThemaId) : undefined;
      
      const result = await generateProfessionalSongtextFromDescription(
        order.beschrijving,
        { 
          temperature: 0.7,
          thema_id: themaId
        }
      );
      
      setSongtext(result.songtext);
      setPrompt('Professionele prompt gebruikt (11,698 karakters)');
      setActiveTab('songtext');
      setIsGenerated(true);
      
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Fout bij het genereren van songtekst');
      console.error('Error generating songtext:', err);
    }
  };

  const handleGeneratePrompt = async () => {
    setIsGenerating(true);
    setError('');
    
    try {
      await generatePromptFromOrder();
    } catch (err) {
      setError('Fout bij het genereren van de prompt');
      console.error('Error generating prompt:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateSongtext = async () => {
    // Dit doet nu hetzelfde als handleGeneratePrompt
    await handleGeneratePrompt();
  };

  const handleCopyToSongtext = () => {
    if (songtext.trim()) {
      onCopyToSongtext(songtext);
    } else if (prompt.trim()) {
      onCopyToSongtext(prompt);
    }
  };

  return (
    <Card className="border-0 shadow-xl bg-gradient-to-br from-blue-50 to-indigo-50 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center justify-between text-gray-800">
          <div className="flex items-center gap-2">
            <FileTextIcon className="h-5 w-5 text-blue-600" />
            AI Generatie
            <span className="text-lg">🤖</span>
          </div>
          {isGenerated && !isGenerating && (
            <Badge variant="outline" className="text-green-600 border-green-200 bg-green-50">
              <CheckIcon className="h-3 w-3 mr-1" />
              Klaar
            </Badge>
          )}
          {isGenerating && (
            <Badge variant="outline" className="text-blue-600 border-blue-200 bg-blue-50">
              <div className="w-3 h-3 border-2 border-blue-600 border-t-transparent rounded-full animate-spin mr-1"></div>
              Genereren...
            </Badge>
          )}
        </CardTitle>
        
        {/* AI Provider and Thema Selection */}
        <div className="flex items-center gap-4 mt-2">
          {/* AI Provider Selection */}
          {providers.length > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">AI Provider:</span>
              <Select value={selectedProvider} onValueChange={setSelectedProvider}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Kies AI provider" />
                </SelectTrigger>
                <SelectContent>
                  {providers.filter(p => p.available).map((provider) => (
                    <SelectItem key={provider.name} value={provider.name}>
                      {provider.display_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
          
          {/* Thema Selection */}
          {themas.length > 0 && (
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">Thema:</span>
              <Select value={selectedThemaId} onValueChange={setSelectedThemaId}>
                <SelectTrigger className="w-48">
                  <SelectValue placeholder="Kies thema (optioneel)" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="">Geen specifiek thema</SelectItem>
                  {themas.map((thema) => (
                    <SelectItem key={thema.id} value={thema.id.toString()}>
                      {thema.display_name}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>
          )}
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Error Display */}
        {error && (
          <div className="p-3 bg-red-50 border border-red-200 rounded-md">
            <p className="text-red-600 text-sm">{error}</p>
          </div>
        )}

        {/* Tab Navigation */}
        <div className="flex space-x-1 bg-gray-100 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('prompt')}
            className={`flex-1 py-2 px-3 text-sm font-medium rounded-md transition-colors ${
              activeTab === 'prompt'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Prompt
          </button>
          <button
            onClick={() => setActiveTab('songtext')}
            className={`flex-1 py-2 px-3 text-sm font-medium rounded-md transition-colors ${
              activeTab === 'songtext'
                ? 'bg-white text-blue-600 shadow-sm'
                : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            Songtekst
          </button>
        </div>

        {/* Tab Content */}
        {activeTab === 'prompt' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Professionele Prompt
              </label>
              <Textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Professionele prompt wordt automatisch gegenereerd..."
                className="min-h-[120px] resize-none"
                readOnly
              />
            </div>
            
            <div className="flex gap-2">
              <Button
                onClick={handleGeneratePrompt}
                disabled={isGenerating || !order.beschrijving}
                className="flex-1 bg-blue-600 hover:bg-blue-700"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Genereren...
                  </>
                ) : (
                  'Genereer Prompt'
                )}
              </Button>
            </div>
          </div>
        )}

        {activeTab === 'songtext' && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gegenereerde Songtekst
              </label>
              <Textarea
                value={songtext}
                onChange={(e) => setSongtext(e.target.value)}
                placeholder="Songtekst wordt hier gegenereerd..."
                className="min-h-[200px] resize-none"
              />
            </div>
            
            <div className="flex gap-2">
              <Button
                onClick={handleGenerateSongtext}
                disabled={isGenerating || !order.beschrijving}
                className="flex-1 bg-green-600 hover:bg-green-700"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Genereren...
                  </>
                ) : (
                  'Genereer Songtekst'
                )}
              </Button>
              
              <Button
                onClick={handleCopyToSongtext}
                disabled={!songtext.trim() && !prompt.trim()}
                variant="outline"
                className="flex-1"
              >
                Gebruik Deze Songtekst
              </Button>
            </div>
          </div>
        )}

        <Separator />

        {/* Info Section */}
        <div className="text-xs text-gray-500 space-y-1">
          <p>• Professionele prompt wordt altijd gebruikt voor optimale resultaten</p>
          <p>• Thema selectie is optioneel - laat leeg voor algemene prompt</p>
          <p>• AI Provider wordt automatisch gekozen op basis van beschikbaarheid</p>
        </div>
      </CardContent>
    </Card>
  );
};

export default AIPromptCard;
