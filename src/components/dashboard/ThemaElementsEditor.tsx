import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { EditIcon, XIcon, EyeIcon, SaveIcon } from '@/components/icons/IconComponents';
import { ThemaElement } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';
import ElementTypeSection from './ElementTypeSection';
import AddElementSection from './AddElementSection';

interface ThemaElementsEditorProps {
  themaId: number;
  elements: ThemaElement[];
  isEditing: boolean;
  onToggleEdit: () => void;
  onElementsChange: () => void;
}

const ThemaElementsEditor: React.FC<ThemaElementsEditorProps> = ({ 
  themaId, 
  elements, 
  isEditing, 
  onToggleEdit,
  onElementsChange 
}) => {
  const [expandedSections, setExpandedSections] = useState<Set<string>>(new Set());
  const { toast } = useToast();

  // Group elements by type
  const elementsByType = elements.reduce((acc, element) => {
    if (!acc[element.element_type]) {
      acc[element.element_type] = [];
    }
    acc[element.element_type].push(element);
    return acc;
  }, {} as Record<string, ThemaElement[]>);

  const toggleSection = (elementType: string) => {
    const newExpanded = new Set(expandedSections);
    if (newExpanded.has(elementType)) {
      newExpanded.delete(elementType);
    } else {
      newExpanded.add(elementType);
    }
    setExpandedSections(newExpanded);
  };

  const handleToggleEdit = () => {
    if (isEditing) {
      toast({
        title: "Bewerkingsmodus uitgezet",
        description: "Je kunt nu elementen bekijken zonder te bewerken"
      });
    } else {
      toast({
        title: "Bewerkingsmodus ingeschakeld",
        description: "Je kunt nu elementen bewerken, toevoegen en verwijderen"
      });
    }
    onToggleEdit();
  };

  const totalElements = elements.length;
  const elementTypes = Object.keys(elementsByType).length;

  return (
    <div className="space-y-6">
      {/* Header with edit toggle and summary */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <h3 className="text-lg font-semibold text-gray-900">Thema Elementen</h3>
          <div className="flex gap-2">
            <Badge variant="outline" className="text-xs">
              {totalElements} elementen
            </Badge>
            <Badge variant="outline" className="text-xs">
              {elementTypes} types
            </Badge>
          </div>
        </div>
        <Button
          variant={isEditing ? "destructive" : "default"}
          size="sm"
          onClick={handleToggleEdit}
        >
          {isEditing ? (
            <>
              <XIcon className="h-4 w-4 mr-2" />
              Stoppen met bewerken
            </>
          ) : (
            <>
              <EditIcon className="h-4 w-4 mr-2" />
              Bewerken
            </>
          )}
        </Button>
      </div>

      {/* Edit mode notice */}
      {isEditing && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center gap-2 text-blue-800">
            <EditIcon className="h-4 w-4" />
            <span className="text-sm font-medium">Bewerkingsmodus actief</span>
          </div>
          <p className="text-sm text-blue-700 mt-1">
            Je kunt nu elementen bewerken, toevoegen en verwijderen. Klik op de bewerk-knop naast elk element om het te wijzigen.
          </p>
        </div>
      )}

      {/* Element type sections */}
      <div className="space-y-4">
        {Object.keys(elementsByType).length === 0 ? (
          <Card className="bg-gray-50">
            <CardContent className="p-8 text-center">
              <div className="text-gray-500 mb-4">
                <EyeIcon className="h-8 w-8 mx-auto mb-2" />
                <p className="text-sm">Geen elementen gevonden voor dit thema</p>
              </div>
              {isEditing && (
                <p className="text-xs text-gray-400">
                  Gebruik de sectie hieronder om nieuwe elementen toe te voegen
                </p>
              )}
            </CardContent>
          </Card>
        ) : (
          Object.entries(elementsByType)
            .sort(([a], [b]) => {
              // Sort element types in a logical order
              const order = ['keyword', 'power_phrase', 'genre', 'bpm', 'key', 'instrument', 'effect', 'verse_starter', 'rhyme_word'];
              const aIndex = order.indexOf(a);
              const bIndex = order.indexOf(b);
              if (aIndex === -1 && bIndex === -1) return a.localeCompare(b);
              if (aIndex === -1) return 1;
              if (bIndex === -1) return -1;
              return aIndex - bIndex;
            })
            .map(([type, typeElements]) => (
              <ElementTypeSection
                key={type}
                themaId={themaId}
                elementType={type}
                elements={typeElements}
                isEditing={isEditing}
                onElementsChange={onElementsChange}
              />
            ))
        )}
      </div>

      {/* Add new element section */}
      {isEditing && (
        <AddElementSection
          themaId={themaId}
          onElementsChange={onElementsChange}
        />
      )}

      {/* Summary footer */}
      <div className="border-t pt-4">
        <div className="flex justify-between items-center text-sm text-gray-600">
          <span>
            Laatste wijziging: {new Date().toLocaleString('nl-NL')}
          </span>
          <span>
            {totalElements} elementen in {elementTypes} categorieën
          </span>
        </div>
      </div>
    </div>
  );
};

export default ThemaElementsEditor; 