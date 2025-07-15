
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
  const [useProfessional, setUseProfessional] = useState(false);

  // Bepaal of dit een STANDARD order is
  const isStandardOrder = order.typeOrder === 'STANDARD';

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
    
    // Automatisch professionele prompt voor STANDARD orders
    if (isStandardOrder) {
      setUseProfessional(true);
    }
  }, [isStandardOrder]);

  const generatePromptFromOrder = async () => {
    if (!order.beschrijving) {
      setError('Geen beschrijving beschikbaar in de order');
      return;
    }

    try {
      if (useProfessional) {
        // Gebruik professionele prompt endpoint
        const result = await generateProfessionalSongtextFromDescription(
          order.beschrijving,
          { temperature: 0.7 }
        );
        
        // De professionele endpoint geeft direct een songtekst terug
        setSongtext(result.songtext);
        setPrompt('Professionele prompt gebruikt (11,698 karakters)');
        setActiveTab('songtext');
      } else {
        // Gebruik gewone prompt endpoint
        const result = await generateSongtextFromDescription(
          order.beschrijving,
          selectedProvider || undefined,
          { temperature: 0.7 }
        );
        
        setSongtext(result.songtext);
        setPrompt('Gewone prompt gebruikt');
        setActiveTab('songtext');
      }
      
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

  const getPlaceholderText = () => {
    if (isGenerating) {
      return useProfessional ? 
        "Professionele songtekst wordt gegenereerd met uitgebreide prompt..." :
        "Songtekst wordt gegenereerd...";
    }
    return useProfessional ? 
      "Klik 'Genereer Songtekst' om een professionele Nederlandse songtekst te genereren" :
      "Klik 'Genereer Songtekst' om een songtekst te genereren";
  };

  const getPromptInfoText = () => {
    if (useProfessional) {
      return "🎨 Professionele prompt - gebruikt uitgebreide template met voorbeelden van Annie M.G. Schmidt, Andre Hazes, Stef Bos, etc.";
    }
    return "📝 Standaard prompt - basis Nederlandse songtekst generatie";
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
            <Select value={selectedProvider} onValueChange={setSelectedProvider} disabled={useProfessional}>
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
        
        {/* Professional Prompt Toggle */}
        <div className="flex items-center justify-between bg-gray-50 p-3 rounded-lg mt-3">
          <div className="flex items-center space-x-2">
            <input
              type="checkbox"
              id="professional-prompt"
              checked={useProfessional}
              onChange={(e) => setUseProfessional(e.target.checked)}
              className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500"
            />
            <label htmlFor="professional-prompt" className="text-sm font-medium text-gray-700">
              Professionele Prompt
            </label>
            {isStandardOrder && (
              <Badge variant="secondary" className="text-xs">
                Auto voor STANDARD
              </Badge>
            )}
          </div>
          <div className="text-xs text-gray-500 max-w-md">
            {getPromptInfoText()}
          </div>
        </div>
        
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
            <div className="bg-gray-50 p-4 rounded-lg border">
              <h3 className="font-medium text-gray-700 mb-2">Prompt Informatie</h3>
              <p className="text-sm text-gray-600 mb-3">
                {useProfessional 
                  ? "Er wordt een uitgebreide professionele prompt gebruikt met 11,698 karakters, inclusief voorbeelden van Nederlandse artiesten en specifieke stijlrichtlijnen."
                  : "Er wordt een basis prompt gebruikt voor Nederlandse songtekst generatie."
                }
              </p>
              
              {order.beschrijving && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Order beschrijving:</h4>
                  <p className="text-sm text-gray-600 italic">"{order.beschrijving}"</p>
                </div>
              )}
              
              <div className="text-xs text-gray-500">
                {useProfessional 
                  ? "🎨 Professionele prompt actief - A2 taalniveau, natuurlijk rijm, 5-6 lettergrepen per regel"
                  : "📝 Basis prompt actief - standaard Nederlandse songtekst generatie"
                }
              </div>
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3">
              <Button 
                onClick={handleGeneratePrompt}
                disabled={isGenerating || !order.beschrijving}
                className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
              >
                {isGenerating ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    {useProfessional ? 'Professionele songtekst genereren...' : 'Songtekst genereren...'}
                  </>
                ) : (
                  <>
                    🎵 {useProfessional ? 'Genereer Professionele Songtekst' : 'Genereer Songtekst'}
                  </>
                )}
              </Button>
              
              {!order.beschrijving && (
                <div className="text-sm text-red-600">
                  Geen beschrijving beschikbaar in de order
                </div>
              )}
            </div>
          </>
        )}
        
        {activeTab === 'songtext' && (
          <>
            <Textarea
              value={songtext}
              onChange={(e) => setSongtext(e.target.value)}
              placeholder={songtext ? "" : "Nog geen songtekst gegenereerd. Klik op 'Genereer Songtekst' om te beginnen."}
              className="min-h-[300px] max-h-[400px] text-sm leading-relaxed border-gray-200 focus:border-blue-500 focus:ring-blue-500 resize-none"
              disabled={isGenerating}
            />
            
            <div className="flex flex-col sm:flex-row gap-3">
              {!songtext.trim() && (
                <Button 
                  onClick={handleGenerateSongtext}
                  disabled={isGenerating || !order.beschrijving}
                  className="flex-1 bg-purple-600 hover:bg-purple-700 text-white"
                >
                  {isGenerating ? (
                    <>
                      <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                      {useProfessional ? 'Professionele songtekst genereren...' : 'Songtekst genereren...'}
                    </>
                  ) : (
                    <>
                      🎵 {useProfessional ? 'Genereer Professionele Songtekst' : 'Genereer Songtekst'}
                    </>
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
              
              {!order.beschrijving && (
                <div className="text-sm text-red-600">
                  Geen beschrijving beschikbaar in de order
                </div>
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
