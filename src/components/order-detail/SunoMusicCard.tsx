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
  { value: 'blues', label: 'Blues' }
];

export const SunoMusicCard: React.FC<SunoMusicCardProps> = ({ order, currentSongtext }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [musicResult, setMusicResult] = useState<MusicResponse | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentAudio, setCurrentAudio] = useState<HTMLAudioElement | null>(null);
  const [localSongtext, setLocalSongtext] = useState('');
  
  // Form state
  const [style, setStyle] = useState('');
  const [instrumental, setInstrumental] = useState(false);
  const [customTitle, setCustomTitle] = useState('');
  
  const { toast } = useToast();

  // Update local songtext when currentSongtext changes
  useEffect(() => {
    setLocalSongtext(currentSongtext || order.songtekst || order.beschrijving || '');
  }, [currentSongtext, order.songtekst, order.beschrijving]);

  const canGenerateMusic = localSongtext.length > 50;

  // Auto-determine style based on order theme
  const getDefaultStyle = (): string => {
    if (style) return style; // User selected style takes precedence
    
    const themeStyles: { [key: string]: string } = {
      'verjaardag': 'pop',
      'liefde': 'acoustic',
      'huwelijk': 'romantic',
      'afscheid': 'ballad',
      'vaderdag': 'folk',
      'anders': 'pop'
    };
    
    const orderTheme = order.thema?.toLowerCase() || 'anders';
    return themeStyles[orderTheme] || 'pop';
  };

  const handleGenerateMusic = async () => {
    if (!canGenerateMusic) {
      toast({
        title: "Geen songtekst",
        description: "De songtekst is te kort om muziek van te maken (minimaal 50 karakters).",
        variant: "destructive"
      });
      return;
    }

    setIsGenerating(true);
    try {
      const result = await aiApi.generateMusic({
        songtext: localSongtext,
        style: getDefaultStyle(),
        instrumental: instrumental,
        title: customTitle || `Lied voor ${order.klant_naam || 'onbekend'}`
      });

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
      toast({
        title: "Muziekgeneratie mislukt",
        description: error instanceof Error ? error.message : "Er ging iets mis bij het genereren van muziek.",
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
              Suno AI
            </Badge>
          </div>
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setIsExpanded(!isExpanded)}
            className="text-purple-600 hover:text-purple-800"
          >
            {isExpanded ? <ArrowUpIcon className="h-4 w-4" /> : <ChevronDownIcon className="h-4 w-4" />}
          </Button>
        </CardTitle>
      </CardHeader>
      
      <CardContent className="space-y-4">
        {/* Songtext preview - now editable */}
        <div className="bg-white p-3 rounded-lg border">
          <div className="flex items-center justify-between mb-2">
            <Label className="text-sm font-medium text-gray-700">
              Songtekst voor muziekgeneratie:
            </Label>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className={`text-xs ${canGenerateMusic ? 'text-green-600 bg-green-50' : 'text-red-600 bg-red-50'}`}>
                {localSongtext.length} karakters
              </Badge>
              {currentSongtext && (
                <Badge variant="outline" className="text-xs text-blue-600 bg-blue-50">
                  🔄 Gesynchroniseerd
                </Badge>
              )}
            </div>
          </div>
          <Textarea
            value={localSongtext}
            onChange={(e) => setLocalSongtext(e.target.value)}
            className="resize-none h-24 text-sm"
            placeholder="Geen songtekst beschikbaar - ga naar de Songtekst tab om een songtekst te genereren of op te slaan"
          />
          {!canGenerateMusic && (
            <p className="text-xs text-red-600 mt-2">
              ⚠️ Minimaal 50 karakters nodig voor muziekgeneratie
            </p>
          )}
        </div>

        {/* Music generation controls */}
        {isExpanded && (
          <div className="space-y-4 pt-4 border-t">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Style selection */}
              <div>
                <Label htmlFor="style" className="text-sm font-medium">
                  Muziekstijl
                </Label>
                <Select value={style} onValueChange={setStyle}>
                  <SelectTrigger>
                    <SelectValue placeholder={`Auto (${getDefaultStyle()})`} />
                  </SelectTrigger>
                  <SelectContent>
                    {MUSIC_STYLES.map((styleOption) => (
                      <SelectItem key={styleOption.value} value={styleOption.value}>
                        {styleOption.label}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              {/* Custom title */}
              <div>
                <Label htmlFor="title" className="text-sm font-medium">
                  Titel (optioneel)
                </Label>
                <Input
                  id="title"
                  value={customTitle}
                  onChange={(e) => setCustomTitle(e.target.value)}
                  placeholder={`Lied voor ${order.klant_naam || 'onbekend'}`}
                />
              </div>
            </div>

            {/* Instrumental toggle */}
            <div className="flex items-center space-x-2">
              <Switch
                id="instrumental"
                checked={instrumental}
                onCheckedChange={setInstrumental}
              />
              <Label htmlFor="instrumental" className="text-sm">
                Alleen instrumentaal (geen zang)
              </Label>
            </div>

            {/* Generate button */}
            <Button
              onClick={handleGenerateMusic}
              disabled={isGenerating || !canGenerateMusic}
              className="w-full bg-purple-600 hover:bg-purple-700 text-white"
            >
              {isGenerating ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2" />
                  Muziek genereren...
                </>
              ) : (
                <>
                  <MusicIcon className="h-4 w-4 mr-2" />
                  Genereer Volledige Muziek
                </>
              )}
            </Button>
          </div>
        )}

        {/* Music result */}
        {musicResult && (
          <div className="bg-white p-4 rounded-lg border border-purple-200 mt-4">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h4 className="font-medium text-gray-900">{musicResult.title}</h4>
                <p className="text-sm text-gray-600">
                  {musicResult.style} • {musicResult.model}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handlePlayPause}
                  className="text-purple-600 border-purple-300 hover:bg-purple-50"
                >
                  {isPlaying ? "⏸️" : "▶️"}
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleDownload}
                  className="text-purple-600 border-purple-300 hover:bg-purple-50"
                >
                  <DownloadIcon className="h-4 w-4" />
                </Button>
              </div>
            </div>

            {/* Audio player */}
            {musicResult.audio_url && (
              <div className="bg-purple-50 p-3 rounded-lg">
                <div className="flex items-center gap-2 text-sm text-purple-700">
                  🔊
                  <span>Klik op play om te beluisteren</span>
                </div>
              </div>
            )}

            {/* Additional info */}
            <div className="text-xs text-gray-500 mt-2">
              Gegenereerd op {new Date(musicResult.generated_at || '').toLocaleString('nl-NL')}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}; 