
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { FileTextIcon, CheckIcon } from '@/components/icons/IconComponents';

interface AIPromptCardProps {
  onCopyToSongtext: (prompt: string) => void;
}

const AIPromptCard: React.FC<AIPromptCardProps> = ({ onCopyToSongtext }) => {
  const [prompt, setPrompt] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [isGenerated, setIsGenerated] = useState(false);

  const handleGeneratePrompt = async () => {
    setIsGenerating(true);
    
    // Dummy delay to simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    const dummyPrompt = `Schrijf een emotioneel lied voor een verjaardag met de volgende elementen:

- Thema: Verjaardag en dankbaarheid
- Toon: Vrolijk en hartverwarmend
- Structuur: Vers-Refrein-Vers-Refrein-Bridge-Refrein
- Persoonlijke elementen: Familie, vriendschap, herinneringen
- Rijmschema: ABAB per vers

Het lied moet een gevoel van warmte en verbondenheid uitstralen, met focus op de bijzondere momenten die we samen hebben gedeeld. Gebruik beeldende taal en concrete herinneringen om het persoonlijk te maken.

Zorg ervoor dat het refrein gemakkelijk mee te zingen is en blijft hangen.`;

    setPrompt(dummyPrompt);
    setIsGenerating(false);
    setIsGenerated(true);
  };

  const handleRegenerate = async () => {
    setIsGenerating(true);
    setIsGenerated(false);
    
    // Dummy delay to simulate API call
    await new Promise(resolve => setTimeout(resolve, 1500));
    
    const regeneratedPrompt = `Creëer een uniek verjaardagslied met deze specificaties:

- Stijl: Moderne pop-ballad met akoestische elementen
- Sfeer: Intiem en persoonlijk, maar hoopvol
- Opbouw: Intro-Vers-Pre-Chorus-Chorus-Vers-Pre-Chorus-Chorus-Bridge-Chorus-Outro
- Tekstuele focus: Persoonlijke groei, mijlpalen, toekomstdromen
- Melodische richtlijn: Gemakkelijk zingbaar, emotioneel impactvol

Het lied moet reflectie combineren met viering, waarbij zowel het verleden als de toekomst worden omarmd. Gebruik metaforen van seizoenen of reis om groei uit te drukken.

Maak het toegankelijk maar diepgaand, met ruimte voor persoonlijke interpretatie.`;

    setPrompt(regeneratedPrompt);
    setIsGenerating(false);
    setIsGenerated(true);
  };

  const handleCopyToSongtext = () => {
    if (prompt.trim()) {
      onCopyToSongtext(prompt);
    }
  };

  const getPlaceholderText = () => {
    if (isGenerating) {
      return "Prompt wordt gegenereerd...";
    }
    return "Nog geen prompt – klik Genereer";
  };

  return (
    <Card className="border-0 shadow-xl bg-white/95 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center justify-between text-gray-800">
          <div className="flex items-center gap-2">
            <FileTextIcon className="h-5 w-5 text-blue-600" />
            AI Prompt
            <span className="text-lg">📝</span>
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
        <Separator />
      </CardHeader>
      <CardContent className="space-y-6">
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
          
          {isGenerated && (
            <Button 
              variant="ghost"
              onClick={handleRegenerate}
              disabled={isGenerating}
              className="border-gray-200 hover:bg-gray-50"
            >
              Hergegenereer
            </Button>
          )}
          
          {prompt.trim() && !isGenerating && (
            <Button 
              onClick={handleCopyToSongtext}
              className="bg-green-600 hover:bg-green-700 text-white"
            >
              Kopieer naar Songtekst
            </Button>
          )}
        </div>

        {isGenerated && prompt && (
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="flex items-center gap-2 mb-2">
              <CheckIcon className="h-4 w-4 text-blue-600" />
              <span className="text-sm font-medium text-blue-800">
                Prompt gegenereerd
              </span>
            </div>
            <p className="text-sm text-blue-700">
              De prompt is {prompt.split('\n').length} regels lang en bevat {prompt.length} karakters. 
              Je kunt de tekst handmatig aanpassen voordat je deze kopieert naar de songtekst editor.
            </p>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AIPromptCard;
