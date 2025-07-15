import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Switch } from '@/components/ui/switch';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { aiApi, MusicResponse } from '@/services/aiApi';
import { Order } from '@/types';
import { ChevronDownIcon, ArrowUpIcon, MusicIcon, DownloadIcon, XIcon } from '@/components/icons/IconComponents';

interface SunoMusicCardProps {
  order: Order;
  currentSongtext?: string; // Add prop for current songtext from editor
}

const MUSIC_STYLES = [
  { value: 'pop', label: 'Pop' },
  { value: 'acoustic', label: 'Akoestisch' },
  { value: 'jazz', label: 'Jazz' },
  { value: 'rock', label: 'Rock' },
  { value: 'ballad', label: 'Ballad' },
  { value: 'folk', label: 'Folk' },
  { value: 'romantic', label: 'Romantisch' },
  { value: 'classical', label: 'Klassiek' },
  { value: 'country', label: 'Country' },
  { value: 'blues', label: 'Blues' },
  { value: 'electronic', label: 'Electronic' },
  { value: 'rap', label: 'Rap' },
  { value: 'indie', label: 'Indie' },
  { value: 'reggae', label: 'Reggae' },
  { value: 'latin', label: 'Latin' }
];

const SUNO_MODELS = [
  { value: 'V4_5', label: 'V4.5 (Beste, tot 8 min)', description: 'Superior genre blending, snelste output' },
  { value: 'V4', label: 'V4 (Hoge kwaliteit, tot 4 min)', description: 'Beste audiokwaliteit, verfijnde structuur' },
  { value: 'V3_5', label: 'V3.5 (Creatief, tot 4 min)', description: 'Solide arrangementen, creatieve diversiteit' }
];

export const SunoMusicCard: React.FC<SunoMusicCardProps> = ({ order, currentSongtext }) => {
  const [isExpanded, setIsExpanded] = useState(true);
  const [isGenerating, setIsGenerating] = useState(false);
  const [musicResult, setMusicResult] = useState<MusicResponse | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  const [localSongtext, setLocalSongtext] = useState('');
  
  // Custom Mode form state
  const [customMode] = useState(true); // Altijd Custom Mode voor volledige controle
  const [style, setStyle] = useState('');
  const [instrumental, setInstrumental] = useState(false);
  const [customTitle, setCustomTitle] = useState('');
  const [model, setModel] = useState('V4_5');
  const [negativeTags, setNegativeTags] = useState('');
  
  const { toast } = useToast();

  // Update local songtext when currentSongtext changes
  useEffect(() => {
    setLocalSongtext(currentSongtext || order.songtekst || '');
  }, [currentSongtext, order.songtekst]);

  // Auto-set default values
  useEffect(() => {
    if (!style) {
      const themeStyles: { [key: string]: string } = {
        'verjaardag': 'pop',
        'liefde': 'acoustic',
        'huwelijk': 'romantic',
        'afscheid': 'ballad',
        'vaderdag': 'folk',
        'anders': 'pop'
      };
      const orderTheme = order.thema?.toLowerCase() || 'anders';
      setStyle(themeStyles[orderTheme] || 'pop');
    }
    
    if (!customTitle) {
      setCustomTitle(`Lied voor ${order.klant_naam || 'onbekend'}`);
    }
  }, [order.thema, order.klant_naam, style, customTitle]);

  // Get max character limits based on selected model
  const getCharLimits = () => {
    if (model === 'V4_5') {
      return { prompt: 5000, style: 1000, title: 80 };
    } else {
      return { prompt: 3000, style: 200, title: 80 };
    }
  };

  const charLimits = getCharLimits();
  const canGenerateMusic = !instrumental ? localSongtext.length > 50 : true;
  const isPromptTooLong = localSongtext.length > charLimits.prompt;
  const isStyleTooLong = style.length > charLimits.style;
  const isTitleTooLong = customTitle.length > charLimits.title;

  // Check if all required fields are filled
  const isFormValid = () => {
    if (instrumental) {
      return style.trim() && customTitle.trim() && !isStyleTooLong && !isTitleTooLong;
    } else {
      return style.trim() && customTitle.trim() && localSongtext.trim() && 
             !isPromptTooLong && !isStyleTooLong && !isTitleTooLong;
    }
  };

  const handleGenerateMusic = async () => {
    if (!isFormValid()) {
      toast({
        title: "Onvolledige gegevens",
        description: "Vul alle verplichte velden in en controleer de tekst lengtes.",
        variant: "destructive"
      });
      return;
    }

    setIsGenerating(true);
    try {
      const requestData = {
        customMode: true,
        instrumental: instrumental,
        model: model,
        style: style,
        title: customTitle,
        ...(negativeTags && { negativeTags }),
        ...(instrumental ? {} : { prompt: localSongtext }) // Only add prompt if not instrumental
      };

      const result = await aiApi.generateMusic(requestData);

      if (result.success) {
        setMusicResult(result);
        toast({
          title: "Muziek gegenereerd!",
          description: `"${result.title}" is klaar om te beluisteren.`,
        });
      } else {
        throw new Error(result.error || 'Onbekende fout bij muziekgeneratie');
      }
    } catch (error) {
      console.error('Music generation error:', error);
      
      let errorMessage = "Er ging iets mis bij het genereren van muziek.";
      let errorTitle = "Muziekgeneratie mislukt";
      
      if (error instanceof Error) {
        if (error.message.includes('413') || error.message.includes('Payload Too Large')) {
          errorTitle = "Input te lang";
          errorMessage = "De ingevoerde tekst is te lang voor het geselecteerde model.";
        } else if (error.message.includes('429')) {
          errorTitle = "Te veel verzoeken";
          errorMessage = "Te veel verzoeken naar de muziekservice. Probeer het over een paar minuten opnieuw.";
        } else if (error.message.includes('500')) {
          errorTitle = "Server probleem";
          errorMessage = "Er is een probleem met de muziekgeneratie service. Probeer het later opnieuw.";
        } else {
          errorMessage = error.message;
        }
      }
      
      toast({
        title: errorTitle,
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setIsGenerating(false);
    }
  };

  const handlePlayPause = () => {
    if (!musicResult?.audio_url) return;

    if (currentAudio) {
      if (isPlaying) {
        currentAudio.pause();
        setIsPlaying(false);
      } else {
        currentAudio.play();
        setIsPlaying(true);
      }
    } else {
      const audio = new Audio(musicResult.audio_url);
      audio.addEventListener('ended', () => {
        setIsPlaying(false);
      });
      audio.addEventListener('error', () => {
        toast({
          title: "Afspeel fout",
          description: "Kon de muziek niet afspelen.",
          variant: "destructive"
        });
        setIsPlaying(false);
      });
      
      setCurrentAudio(audio);
      audio.play();
      setIsPlaying(true);
    }
  };

  const handleDownload = () => {
    if (!musicResult?.audio_url) return;
    
    const link = document.createElement('a');
    link.href = musicResult.audio_url;
    link.download = `${musicResult.title || 'song'}.mp3`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <Card className="mt-6 border-2 border-purple-200 bg-gradient-to-br from-purple-50 to-pink-50">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <MusicIcon className="h-5 w-5 text-purple-600" />
            <span>Muziek Generatie</span>
            <Badge variant="secondary" className="bg-purple-100 text-purple-800">
              Custom Mode
            </Badge>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
          >
            {isExpanded ? <ArrowUpIcon className="h-4 w-4" /> : <ChevronDownIcon className="h-4 w-4" />}
          </Button>
        </CardTitle>
      </CardHeader>
      
      {isExpanded && (
        <CardContent className="space-y-6">
          {/* Model Selection */}
          <div className="space-y-2">
            <Label htmlFor="model-select" className="text-sm font-medium">
              Model <span className="text-red-500">*</span>
            </Label>
            <Select value={model} onValueChange={setModel}>
              <SelectTrigger>
                <SelectValue placeholder="Selecteer model" />
              </SelectTrigger>
              <SelectContent>
                {SUNO_MODELS.map((modelOption) => (
                  <SelectItem key={modelOption.value} value={modelOption.value}>
                    <div>
                      <div className="font-medium">{modelOption.label}</div>
                      <div className="text-xs text-gray-500">{modelOption.description}</div>
                    </div>
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          {/* Title Input */}
          <div className="space-y-2">
            <Label htmlFor="title-input" className="text-sm font-medium">
              Titel <span className="text-red-500">*</span>
              <span className="text-gray-500 text-xs ml-2">
                ({customTitle.length}/{charLimits.title})
              </span>
            </Label>
            <Input
              id="title-input"
              value={customTitle}
              onChange={(e) => setCustomTitle(e.target.value)}
              placeholder="Titel van het lied"
              className={isTitleTooLong ? "border-red-500" : ""}
            />
            {isTitleTooLong && (
              <p className="text-red-500 text-xs">Titel te lang (max {charLimits.title} karakters)</p>
            )}
          </div>

          {/* Style Input */}
          <div className="space-y-2">
            <Label htmlFor="style-select" className="text-sm font-medium">
              Stijl <span className="text-red-500">*</span>
              <span className="text-gray-500 text-xs ml-2">
                ({style.length}/{charLimits.style})
              </span>
            </Label>
            <div className="flex gap-2">
              <Select value={style} onValueChange={setStyle}>
                <SelectTrigger className="flex-1">
                  <SelectValue placeholder="Selecteer stijl" />
                </SelectTrigger>
                <SelectContent>
                  {MUSIC_STYLES.map((styleOption) => (
                    <SelectItem key={styleOption.value} value={styleOption.value}>
                      {styleOption.label}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <Input
                value={style}
                onChange={(e) => setStyle(e.target.value)}
                placeholder="Of typ eigen stijl"
                className={`flex-1 ${isStyleTooLong ? "border-red-500" : ""}`}
              />
            </div>
            {isStyleTooLong && (
              <p className="text-red-500 text-xs">Stijl te lang (max {charLimits.style} karakters)</p>
            )}
          </div>

          {/* Instrumental Toggle */}
          <div className="flex items-center space-x-2">
            <Switch
              id="instrumental-switch"
              checked={instrumental}
              onCheckedChange={setInstrumental}
            />
            <Label htmlFor="instrumental-switch" className="text-sm font-medium">
              Instrumentaal (zonder zang)
            </Label>
          </div>

          {/* Songtext Input - only show if not instrumental */}
          {!instrumental && (
            <div className="space-y-2">
              <Label htmlFor="songtext-input" className="text-sm font-medium">
                Songtekst <span className="text-red-500">*</span>
                <span className="text-gray-500 text-xs ml-2">
                  ({localSongtext.length}/{charLimits.prompt})
                </span>
              </Label>
              <Textarea
                id="songtext-input"
                value={localSongtext}
                onChange={(e) => setLocalSongtext(e.target.value)}
                placeholder="Plak hier de songtekst die je wilt gebruiken voor de muziek..."
                className={`min-h-[200px] ${isPromptTooLong ? "border-red-500" : ""}`}
                disabled={isGenerating}
              />
              {isPromptTooLong && (
                <p className="text-red-500 text-xs">
                  Songtekst te lang voor {model} model (max {charLimits.prompt} karakters)
                </p>
              )}
              {localSongtext.length < 50 && localSongtext.length > 0 && (
                <p className="text-amber-600 text-xs">
                  Songtekst is kort (minimaal 50 karakters aanbevolen)
                </p>
              )}
            </div>
          )}

          {/* Negative Tags */}
          <div className="space-y-2">
            <Label htmlFor="negative-tags" className="text-sm font-medium">
              Negatieve Tags <span className="text-gray-500">(optioneel)</span>
            </Label>
            <Input
              id="negative-tags"
              value={negativeTags}
              onChange={(e) => setNegativeTags(e.target.value)}
              placeholder="Stijlen om te vermijden, bijv: Heavy Metal, Upbeat Drums"
            />
            <p className="text-xs text-gray-500">
              Specificeer stijlen of eigenschappen die je wilt vermijden in de muziek
            </p>
          </div>

          {/* Generate Button */}
          <Button
            onClick={handleGenerateMusic}
            disabled={!isFormValid() || isGenerating}
            className="w-full bg-purple-600 hover:bg-purple-700 text-white"
          >
            {isGenerating ? "Muziek genereren..." : "🎵 Genereer Muziek"}
          </Button>

          {/* Music Result */}
          {musicResult && (
            <div className="mt-6 p-4 bg-white rounded-lg border-2 border-purple-100">
              <div className="flex items-center justify-between mb-3">
                <h3 className="font-medium text-purple-800">
                  {musicResult.title}
                </h3>
                <Badge variant="secondary" className="bg-green-100 text-green-800">
                  {musicResult.model}
                </Badge>
              </div>
              
              {musicResult.style && (
                <p className="text-sm text-gray-600 mb-3">
                  Stijl: {musicResult.style}
                </p>
              )}
              
              <div className="flex gap-2">
                <Button
                  onClick={handlePlayPause}
                  variant="outline"
                  size="sm"
                  className="flex-1"
                >
                  {isPlaying ? "⏸️ Pauzeer" : "▶️ Afspelen"}
                </Button>
                <Button
                  onClick={handleDownload}
                  variant="outline"
                  size="sm"
                  className="flex-1"
                >
                  <DownloadIcon className="h-4 w-4 mr-1" />
                  Download
                </Button>
              </div>
            </div>
          )}
        </CardContent>
      )}
    </Card>
  );
}; 