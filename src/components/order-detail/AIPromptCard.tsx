
import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { FileTextIcon, CheckIcon } from '@/components/icons/IconComponents';
import { aiApi, generateSongtextFromPrompt, type AIProvider } from '@/services/aiApi';
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
  const [error, setError] = useState<string>('');
  const [activeTab, setActiveTab] = useState<'prompt' | 'songtext'>('prompt');

  // Load providers on component mount
  useEffect(() => {
    const loadProviders = async () => {
      try {
        const providersData = await aiApi.getProviders();
        setProviders(providersData.providers);
        setSelectedProvider(providersData.default_provider);
      } catch (err) {
        console.error('Failed to load AI providers:', err);
        setError('Kon AI providers niet laden');
      }
    };
    
    loadProviders();
  }, []);

  const generatePromptFromOrder = () => {
    // Genereer een basis prompt op basis van order data
    const basePrompt = `Schrijf een emotioneel Nederlands lied met de volgende informatie:

Voor: ${order.voornaam || 'Onbekend'}
Van: ${order.klant_naam || 'Onbekend'}
Thema: ${order.thema || 'Algemeen'}
Beschrijving: ${order.beschrijving || 'Geen beschrijving beschikbaar'}

Instructies:
- Schrijf in het Nederlands
- Maak het persoonlijk en emotioneel
- Gebruik een duidelijke structuur met coupletten en refrein
- Zorg voor een memorabel en meezing-baar refrein
- Verwerk de persoonlijke elementen uit de beschrijving`;

    setPrompt(basePrompt);
    return basePrompt;
  };

  const handleGeneratePrompt = async () => {
    setIsGenerating(true);
    setError('');
    
    try {
      const generatedPrompt = generatePromptFromOrder();
      setPrompt(generatedPrompt);
      setIsGenerated(true);
      setActiveTab('prompt');
    } catch (err) {
      setError('Fout bij het genereren van de prompt');
      console.error('Error generating prompt:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleGenerateSongtext = async () => {
    if (!prompt.trim()) {
      setError('Geen prompt beschikbaar. Genereer eerst een prompt.');
      return;
    }
    
    setIsGenerating(true);
    setError('');
    
    try {
      const result = await generateSongtextFromPrompt(
        prompt,
        selectedProvider || undefined,
        { temperature: 0.7 }
      );
      
      setSongtext(result.songtext);
      setActiveTab('songtext');
      setIsGenerated(true);
    } catch (err) {
      setError('Fout bij het genereren van de songtekst');
      console.error('Error generating songtext:', err);
    } finally {
      setIsGenerating(false);
    }
  };

  const handleCopyToSongtext = () => {
    if (songtext.trim()) {
      onCopyToSongtext(songtext);
    } else if (prompt.trim()) {
      onCopyToSongtext(prompt);
    }
  };

  const getPlaceholderText = () => {
    if (isGenerating) {
      return "Prompt wordt gegenereerd...";
    }
    return "Klik 'Genereer Prompt' om een AI prompt te maken op basis van de order informatie";
  };

  return (
    <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
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
        
        {/* AI Provider Selection */}
        {providers.length > 0 && (
          <div className="flex items-center gap-2 mt-2">
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
        
        {/* Tab Navigation */}
        <div className="flex gap-1 mt-3">
          <button
            onClick={() => setActiveTab('prompt')}
            className={`px-3 py-1 text-sm rounded ${
              activeTab === 'prompt' 
                ? 'bg-blue-100 text-blue-700 font-medium' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            📝 Prompt
          </button>
          <button
            onClick={() => setActiveTab('songtext')}
            className={`px-3 py-1 text-sm rounded ${
              activeTab === 'songtext' 
                ? 'bg-blue-100 text-blue-700 font-medium' 
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            🎵 Songtekst
          </button>
        </div>
        
        <Separator className="mt-3" />
      </CardHeader>
      <CardContent className="space-y-6">
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
            {error}
          </div>
        )}
        
        {/* Content based on active tab */}
        {activeTab === 'prompt' && (
          <>
            <Textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder={getPlaceholderText()}
              className="min-h-[200px] max-h-[300px] font-mono text-sm leading-relaxed border-gray-200 focus:border-blue-500 focus:ring-blue-500 resize-none"
              disabled={isGenerating}
            />
            
            <div className="flex flex-col sm:flex-row gap-3">
              <Button 
                onClick={handleGeneratePrompt}
                disabled={isGenerating}
                className="flex-1 bg-blue-600 hover:bg-blue-700 text-white"
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
              
              {prompt.trim() && !isGenerating && (
                <Button 
                  onClick={handleGenerateSongtext}
                  className="bg-purple-600 hover:bg-purple-700 text-white"
                >
                  🎵 Genereer Songtekst
                </Button>
              )}
            </div>
          </>
        )}
        
        {activeTab === 'songtext' && (
          <>
            <Textarea
              value={songtext}
              onChange={(e) => setSongtext(e.target.value)}
              placeholder={songtext ? "" : "Nog geen songtekst gegenereerd. Ga naar de Prompt tab en genereer eerst een prompt."}
              className="min-h-[300px] max-h-[400px] text-sm leading-relaxed border-gray-200 focus:border-blue-500 focus:ring-blue-500 resize-none"
              disabled={isGenerating}
            />
            
            <div className="flex flex-col sm:flex-row gap-3">
              {!songtext.trim() && prompt.trim() && (
                <Button 
                  onClick={handleGenerateSongtext}
                  disabled={isGenerating}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      Songtekst genereren...
                    </>
                  ) : (
                    '🎵 Genereer Songtekst'
                  )}
                </Button>
              )}
              
              {songtext.trim() && !isGenerating && (
                <>
                  <Button 
                    onClick={handleGenerateSongtext}
                    variant="outline"
                    className="border-gray-200 hover:bg-gray-50"
                  >
                    🔄 Regenereer
                  </Button>
                  <Button 
                    onClick={handleCopyToSongtext}
                    className="bg-green-600 hover:bg-green-700 text-white"
                  >
                    ✅ Gebruik Deze Songtekst
                  </Button>
                </>
              )}
            </div>
          </>
        )}

        {/* Status Information */}
        {(prompt || songtext) && !isGenerating && (
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center gap-2 mb-2">
              <CheckIcon className="h-4 w-4 text-blue-600" />
              <span className="text-sm font-medium text-blue-800">
                {activeTab === 'prompt' ? 'Prompt klaar' : 'Songtekst gegenereerd'}
              </span>
            </div>
            <p className="text-sm text-blue-700">
              {activeTab === 'prompt' ? (
                <>
                  De prompt is {prompt.split('\n').length} regels lang en bevat {prompt.length} karakters. 
                  Je kunt de tekst handmatig aanpassen of een songtekst laten genereren.
                </>
              ) : (
                <>
                  De songtekst is {songtext.split('\n').length} regels lang en bevat {songtext.length} karakters.
                  {selectedProvider && ` Gegenereerd met ${providers.find(p => p.name === selectedProvider)?.display_name || selectedProvider}.`}
                </>
              )}
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AIPromptCard;
