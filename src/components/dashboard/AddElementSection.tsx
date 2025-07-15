import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { PlusIcon } from '@/components/icons/IconComponents';
import { themaApi } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';

interface AddElementSectionProps {
  themaId: number;
  onElementsChange: () => void;
}

const ELEMENT_TYPES = [
  { value: 'keyword', label: 'Keyword', description: 'Belangrijke woorden voor het thema' },
  { value: 'power_phrase', label: 'Power Phrase', description: 'Krachtige zinnen voor refrein/chorus' },
  { value: 'genre', label: 'Genre', description: 'Muziekgenre en stijl' },
  { value: 'bpm', label: 'BPM', description: 'Beats per minute' },
  { value: 'key', label: 'Toonsoort', description: 'Muzikale toonsoort' },
  { value: 'instrument', label: 'Instrument', description: 'Instrumenten en sounds' },
  { value: 'effect', label: 'Effect', description: 'Audio effecten' },
  { value: 'verse_starter', label: 'Verse Starter', description: 'Couplet openers' },
  { value: 'rhyme_word', label: 'Rijmwoord', description: 'Rijmwoorden' },
  { value: 'vocal_descriptor', label: 'Vocale Stijl', description: 'Vocale stijl beschrijving' }
];

const USAGE_CONTEXTS = ['any', 'intro', 'verse', 'chorus', 'bridge', 'outro'];

const AddElementSection: React.FC<AddElementSectionProps> = ({
  themaId,
  onElementsChange
}) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [newElementType, setNewElementType] = useState('keyword');
  const [newElementContent, setNewElementContent] = useState('');
  const [newElementContext, setNewElementContext] = useState('any');
  const [newElementWeight, setNewElementWeight] = useState(1);
  const [newElementSunoFormat, setNewElementSunoFormat] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const handleAddElement = async () => {
    if (!newElementContent.trim()) {
      toast({
        title: "Fout",
        description: "Content mag niet leeg zijn",
        variant: "destructive"
      });
      return;
    }

    setIsLoading(true);
    try {
      await themaApi.createElement({
        thema_id: themaId,
        element_type: newElementType,
        content: newElementContent.trim(),
        usage_context: newElementContext === 'any' ? undefined : newElementContext,
        weight: newElementWeight,
        suno_format: newElementSunoFormat.trim() || undefined
      });
      
      // Reset form
      setNewElementContent('');
      setNewElementContext('any');
      setNewElementWeight(1);
      setNewElementSunoFormat('');
      setIsExpanded(false);
      
      onElementsChange();
      
      toast({
        title: "Succes",
        description: "Element succesvol toegevoegd"
      });
    } catch (error) {
      console.error('Error adding element:', error);
      toast({
        title: "Fout",
        description: "Kon element niet toevoegen",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setNewElementContent('');
    setNewElementContext('any');
    setNewElementWeight(1);
    setNewElementSunoFormat('');
    setIsExpanded(false);
  };

  const selectedElementType = ELEMENT_TYPES.find(type => type.value === newElementType);

  return (
    <Card className="bg-gradient-to-br from-green-50 to-emerald-100 border-green-200">
      <CardHeader className="pb-3">
        <CardTitle className="text-sm font-medium text-green-800 flex items-center gap-2">
          <PlusIcon className="h-4 w-4" />
          Nieuw Element Toevoegen
        </CardTitle>
      </CardHeader>
      <CardContent className="pt-0">
        {!isExpanded ? (
          <Button
            variant="outline"
            size="sm"
            onClick={() => setIsExpanded(true)}
            className="w-full border-green-300 text-green-700 hover:bg-green-50"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Element Toevoegen
          </Button>
        ) : (
          <div className="space-y-4">
            {/* Element Type Selection */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Type Element</label>
              <Select value={newElementType} onValueChange={setNewElementType}>
                <SelectTrigger className="w-full">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {ELEMENT_TYPES.map((type) => (
                    <SelectItem key={type.value} value={type.value}>
                      <div className="flex flex-col items-start">
                        <span className="font-medium">{type.label}</span>
                        <span className="text-xs text-gray-500">{type.description}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              {selectedElementType && (
                <p className="text-xs text-gray-600">{selectedElementType.description}</p>
              )}
            </div>

            {/* Content Input */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">Content</label>
              <Input
                placeholder={`Voer ${selectedElementType?.label.toLowerCase()} in...`}
                value={newElementContent}
                onChange={(e) => setNewElementContent(e.target.value)}
                disabled={isLoading}
              />
            </div>

            {/* Advanced Options */}
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Context</label>
                <Select value={newElementContext} onValueChange={setNewElementContext}>
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {USAGE_CONTEXTS.map((context) => (
                      <SelectItem key={context} value={context}>
                        {context}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium text-gray-700">Weight</label>
                <Select 
                  value={newElementWeight.toString()} 
                  onValueChange={(value) => setNewElementWeight(parseInt(value))}
                >
                  <SelectTrigger>
                    <SelectValue />
                  </SelectTrigger>
                  <SelectContent>
                    {[1, 2, 3, 4, 5].map((weight) => (
                      <SelectItem key={weight} value={weight.toString()}>
                        {weight}
                      </SelectItem>
                    ))}
                  </SelectContent>
                </Select>
              </div>
            </div>

            {/* Suno Format (optional) */}
            <div className="space-y-2">
              <label className="text-sm font-medium text-gray-700">
                Suno Format 
                <span className="text-xs text-gray-500 font-normal">(optioneel)</span>
              </label>
              <Input
                placeholder="bijv. [piano], [upbeat], etc."
                value={newElementSunoFormat}
                onChange={(e) => setNewElementSunoFormat(e.target.value)}
                disabled={isLoading}
              />
            </div>

            {/* Action Buttons */}
            <div className="flex gap-2 pt-2">
              <Button
                size="sm"
                onClick={handleAddElement}
                disabled={!newElementContent.trim() || isLoading}
                className="flex-1"
              >
                <PlusIcon className="h-4 w-4 mr-2" />
                Toevoegen
              </Button>
              <Button
                size="sm"
                variant="outline"
                onClick={handleCancel}
                disabled={isLoading}
              >
                Annuleren
              </Button>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default AddElementSection; 