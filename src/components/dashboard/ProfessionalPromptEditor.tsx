import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Separator } from '@/components/ui/separator';
import { EditIcon, XIcon, SaveIcon, EyeIcon, FileTextIcon } from '@/components/icons/IconComponents';
import { Thema, themaApi } from '@/services/themaApi';
import { useToast } from '@/hooks/use-toast';

interface ProfessionalPromptEditorProps {
  thema: Thema;
  isEditing: boolean;
  onToggleEdit: () => void;
  onPromptUpdated: () => void;
}

const ProfessionalPromptEditor: React.FC<ProfessionalPromptEditorProps> = ({ 
  thema, 
  isEditing, 
  onToggleEdit,
  onPromptUpdated 
}) => {
  const [editedPrompt, setEditedPrompt] = useState(thema.professional_prompt || '');
  const [isLoading, setIsLoading] = useState(false);
  const [showPreview, setShowPreview] = useState(false);
  const { toast } = useToast();

  const handleSave = async () => {
    if (editedPrompt.trim() === (thema.professional_prompt || '')) {
      onToggleEdit();
      return;
    }

    setIsLoading(true);
    try {
      await themaApi.updateThema(thema.id, {
        professional_prompt: editedPrompt.trim() || undefined
      });
      
      onPromptUpdated();
      onToggleEdit();
      
      toast({
        title: "Succes",
        description: "Professionele prompt succesvol bijgewerkt"
      });
    } catch (error) {
      console.error('Error updating professional prompt:', error);
      toast({
        title: "Fout",
        description: "Kon professionele prompt niet bijwerken",
        variant: "destructive"
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleCancel = () => {
    setEditedPrompt(thema.professional_prompt || '');
    onToggleEdit();
  };

  const getPromptStats = () => {
    const prompt = isEditing ? editedPrompt : (thema.professional_prompt || '');
    return {
      characters: prompt.length,
      words: prompt.trim() ? prompt.trim().split(/\s+/).length : 0,
      lines: prompt.split('\n').length
    };
  };

  const stats = getPromptStats();

  return (
    <Card className="border-0 shadow-sm">
      <CardHeader className="pb-3">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            <CardTitle className="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <FileTextIcon className="h-5 w-5 text-purple-600" />
              Professionele Prompt
            </CardTitle>
            <div className="flex gap-2">
              <Badge variant="outline" className="text-xs">
                {stats.characters} karakters
              </Badge>
              <Badge variant="outline" className="text-xs">
                {stats.words} woorden
              </Badge>
              <Badge variant="outline" className="text-xs">
                {stats.lines} regels
              </Badge>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {!isEditing && (
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowPreview(!showPreview)}
                className="text-blue-600 hover:text-blue-800"
              >
                <EyeIcon className="h-4 w-4 mr-2" />
                {showPreview ? 'Verberg' : 'Bekijk'}
              </Button>
            )}
            <Button
              variant={isEditing ? "destructive" : "default"}
              size="sm"
              onClick={isEditing ? handleCancel : onToggleEdit}
              disabled={isLoading}
            >
              {isEditing ? (
                <>
                  <XIcon className="h-4 w-4 mr-2" />
                  Annuleren
                </>
              ) : (
                <>
                  <EditIcon className="h-4 w-4 mr-2" />
                  Bewerken
                </>
              )}
            </Button>
          </div>
        </div>
      </CardHeader>
      
      <CardContent className="pt-0">
        {/* Edit mode notice */}
        {isEditing && (
          <div className="bg-purple-50 border border-purple-200 rounded-lg p-4 mb-4">
            <div className="flex items-center gap-2 text-purple-800">
              <EditIcon className="h-4 w-4" />
              <span className="text-sm font-medium">Bewerkingsmodus actief</span>
            </div>
            <p className="text-sm text-purple-700 mt-1">
              Bewerk de professionele prompt voor dit thema. Deze wordt gebruikt bij AI-generatie voor betere resultaten.
            </p>
          </div>
        )}

        {/* Content */}
        {isEditing ? (
          <div className="space-y-4">
            <Textarea
              value={editedPrompt}
              onChange={(e) => setEditedPrompt(e.target.value)}
              placeholder="Voer hier de professionele prompt in voor dit thema..."
              className="min-h-[400px] text-sm font-mono leading-relaxed"
              disabled={isLoading}
            />
            
            <div className="flex items-center justify-between">
              <div className="text-sm text-gray-500">
                💡 Tip: Gebruik specifieke voorbeelden en stijlrichtlijnen voor dit thema
              </div>
              <Button 
                onClick={handleSave}
                disabled={isLoading}
                className="bg-purple-600 hover:bg-purple-700 text-white"
              >
                {isLoading ? (
                  <>
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    Opslaan...
                  </>
                ) : (
                  <>
                    <SaveIcon className="h-4 w-4 mr-2" />
                    Opslaan
                  </>
                )}
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4">
            {!thema.professional_prompt ? (
              <div className="text-center py-8">
                <div className="text-gray-500 mb-4">
                  <FileTextIcon className="h-8 w-8 mx-auto mb-2 text-gray-400" />
                  <p className="text-sm">Geen professionele prompt ingesteld</p>
                </div>
                <p className="text-xs text-gray-400 max-w-md mx-auto">
                  Voeg een professionele prompt toe om betere AI-resultaten te krijgen voor dit thema
                </p>
              </div>
            ) : (
              <>
                <div className="bg-gray-50 p-4 rounded-lg">
                  <div className="flex items-center gap-2 mb-2">
                    <span className="text-sm font-medium text-gray-700">Status:</span>
                    <Badge variant="default" className="bg-green-100 text-green-800">
                      ✅ Professionele prompt actief
                    </Badge>
                  </div>
                  <p className="text-sm text-gray-600">
                    Dit thema heeft een professionele prompt van {stats.characters} karakters. 
                    Deze wordt automatisch gebruikt voor AI-generatie.
                  </p>
                </div>
                
                {showPreview && (
                  <>
                    <Separator />
                    <div className="space-y-3">
                      <div className="flex items-center gap-2">
                        <span className="text-sm font-medium text-gray-700">Prompt Preview:</span>
                        <Badge variant="outline" className="text-xs">
                          Eerste 500 karakters
                        </Badge>
                      </div>
                      <div className="bg-gray-50 p-4 rounded-lg border">
                        <pre className="text-xs text-gray-700 whitespace-pre-wrap font-mono leading-relaxed">
                          {thema.professional_prompt.substring(0, 500)}
                          {thema.professional_prompt.length > 500 && '...'}
                        </pre>
                      </div>
                      {thema.professional_prompt.length > 500 && (
                        <p className="text-xs text-gray-500 text-center">
                          Klik op "Bewerken" om de volledige prompt te zien
                        </p>
                      )}
                    </div>
                  </>
                )}
              </>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default ProfessionalPromptEditor; 