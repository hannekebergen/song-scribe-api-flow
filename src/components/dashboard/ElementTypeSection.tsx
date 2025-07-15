import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { PlusIcon } from '@/components/icons/IconComponents';
import { ThemaElement, themaApi } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';
import ElementItem from './ElementItem';

interface ElementTypeSectionProps {
  themaId: number;
  elementType: string;
  elements: ThemaElement[];
  isEditing: boolean;
  onElementsChange: () => void;
}

const ELEMENT_TYPE_DESCRIPTIONS: Record<string, string> = {
  'keyword': 'Belangrijke woorden voor het thema',
  'power_phrase': 'Krachtige zinnen voor refrein/chorus',
  'genre': 'Muziekgenre en stijl',
  'bpm': 'Beats per minute',
  'key': 'Toonsoort',
  'instrument': 'Instrumenten en sounds',
  'effect': 'Audio effecten',
  'verse_starter': 'Couplet openers',
  'rhyme_word': 'Rijmwoorden',
  'vocal_descriptor': 'Vocale stijl beschrijving'
};

const USAGE_CONTEXTS = ['any', 'intro', 'verse', 'chorus', 'bridge', 'outro'];

const ElementTypeSection: React.FC<ElementTypeSectionProps> = ({
  themaId,
  elementType,
  elements,
  isEditing,
  onElementsChange
}) => {
  const [newElementContent, setNewElementContent] = useState('');
  const [newElementContext, setNewElementContext] = useState<string>('any');
  const [newElementWeight, setNewElementWeight] = useState(1);
  const [isLoading, setIsLoading] = useState(false);
  const { toast } = useToast();

  const getElementTypeDescription = (type: string): string => {
    return ELEMENT_TYPE_DESCRIPTIONS[type] || 'Thema element';
  };

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
        element_type: elementType,
        content: newElementContent.trim(),
        usage_context: newElementContext === 'any' ? undefined : newElementContext,
        weight: newElementWeight
      });
      
      setNewElementContent('');
      setNewElementContext('any');
      setNewElementWeight(1);
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

  const handleDeleteElement = async (elementId: number) => {
    // Remove the element from local state immediately for better UX
    onElementsChange();
  };

  return (
    <div className="border rounded-lg p-4 bg-white">
      <div className="flex items-center justify-between mb-3">
        <h4 className="font-medium text-gray-900 capitalize flex items-center gap-2">
          {elementType.replace('_', ' ')} 
          <Badge variant="outline" className="text-xs font-normal">
            {elements.length}
          </Badge>
        </h4>
        <Badge variant="secondary" className="text-xs">
          {getElementTypeDescription(elementType)}
        </Badge>
      </div>

      {/* Existing elements */}
      <div className="space-y-2">
        {elements.length === 0 ? (
          <div className="text-center py-4 text-gray-500 text-sm">
            Geen {elementType.replace('_', ' ')} elementen gevonden
          </div>
        ) : (
          elements.map((element) => (
            <ElementItem
              key={element.id}
              element={element}
              isEditing={isEditing}
              onDelete={() => handleDeleteElement(element.id)}
              onUpdate={onElementsChange}
            />
          ))
        )}
      </div>

      {/* Add new element */}
      {isEditing && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <div className="space-y-3">
            <div className="flex gap-2">
              <Input
                placeholder={`Nieuw ${elementType.replace('_', ' ')} toevoegen...`}
                value={newElementContent}
                onChange={(e) => setNewElementContent(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAddElement()}
                className="flex-1"
                disabled={isLoading}
              />
              <Button
                size="sm"
                onClick={handleAddElement}
                disabled={!newElementContent.trim() || isLoading}
              >
                <PlusIcon className="h-4 w-4" />
              </Button>
            </div>
            
            {/* Advanced options */}
            <div className="flex gap-2 text-sm">
              <div className="flex items-center gap-2">
                <label className="text-gray-600">Context:</label>
                <Select 
                  value={newElementContext} 
                  onValueChange={setNewElementContext}
                  disabled={isLoading}
                >
                  <SelectTrigger className="w-24 h-8">
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
              
              <div className="flex items-center gap-2">
                <label className="text-gray-600">Weight:</label>
                <Select 
                  value={newElementWeight.toString()} 
                  onValueChange={(value) => setNewElementWeight(parseInt(value))}
                  disabled={isLoading}
                >
                  <SelectTrigger className="w-16 h-8">
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
          </div>
        </div>
      )}
    </div>
  );
};

export default ElementTypeSection; 