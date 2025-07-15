import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { AlertDialog, AlertDialogAction, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { SearchIcon, EditIcon, TrashIcon, EyeIcon } from '@/components/icons/IconComponents';
import { useThemas, useThemaCRUD, useThemaDetails } from '@/hooks/useThema';
import { Thema, ThemaElement } from '@/services/themaApi';
import ThemaElementsEditor from './ThemaElementsEditor';
import ProfessionalPromptEditor from './ProfessionalPromptEditor';



const ThemaList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedThemaId, setSelectedThemaId] = useState<number | null>(null);
  const [editingElementsId, setEditingElementsId] = useState<number | null>(null);
  const [editingPromptId, setEditingPromptId] = useState<number | null>(null);
  const [activeTab, setActiveTab] = useState<'elements' | 'prompt'>('elements');
  const { themas, loading, error, updateParams } = useThemas();
  const { deleteThema, loading: crudLoading } = useThemaCRUD();
  const { thema: themaDetails, elements, rhymeSets, loading: detailsLoading, refetch: refetchThemaDetails } = useThemaDetails(selectedThemaId);

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    updateParams({ search: value || undefined });
  };

  const handleEdit = (thema: Thema) => {
    setSelectedThemaId(thema.id);
    setEditingElementsId(thema.id);
    setActiveTab('elements');
  };

  const handleView = (thema: Thema) => {
    setSelectedThemaId(thema.id);
    setEditingElementsId(null);
    setEditingPromptId(null);
  };

  const handleToggleElementsEdit = () => {
    setEditingElementsId(editingElementsId === selectedThemaId ? null : selectedThemaId);
  };

  const handleTogglePromptEdit = () => {
    setEditingPromptId(editingPromptId === selectedThemaId ? null : selectedThemaId);
  };

  const handleCloseDialog = () => {
    setSelectedThemaId(null);
    setEditingElementsId(null);
    setEditingPromptId(null);
    setActiveTab('elements');
  };

  const handleDelete = async (thema: Thema) => {
    if (confirm(`Weet je zeker dat je thema '${thema.display_name}' wilt verwijderen?`)) {
      try {
        await deleteThema(thema.id, thema.display_name);
        // Refresh the list after deletion
        updateParams({});
      } catch (error) {
        // Error handling is done in the hook
        console.error('Error deleting thema:', error);
      }
    }
  };

  if (loading) {
    return (
      <Card className="bg-white shadow-sm">
        <CardHeader>
          <div className="flex items-center justify-between">
            <Skeleton className="h-6 w-48" />
            <Skeleton className="h-6 w-20" />
          </div>
          <Skeleton className="h-10 w-full" />
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="flex items-center justify-between p-4 border rounded-lg">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <Skeleton className="h-5 w-32" />
                    <Skeleton className="h-5 w-16" />
                    <Skeleton className="h-5 w-20" />
                  </div>
                  <Skeleton className="h-4 w-64 mb-1" />
                  <Skeleton className="h-3 w-32" />
                </div>
                <div className="flex items-center gap-2">
                  <Skeleton className="h-9 w-9" />
                  <Skeleton className="h-9 w-9" />
                  <Skeleton className="h-9 w-9" />
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className="bg-white shadow-sm">
        <CardContent className="p-6">
          <div className="text-center">
            <p className="text-red-600">Fout bij laden thema's: {error}</p>
            <Button 
              onClick={() => updateParams({})} 
              className="mt-4"
              variant="outline"
            >
              Opnieuw proberen
            </Button>
          </div>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className="bg-white shadow-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold text-gray-800">
            Thema Overzicht
          </CardTitle>
          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
            {themas.length} thema's
          </Badge>
        </div>
        
        {/* Search */}
        <div className="relative">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Zoek thema's..."
            value={searchTerm}
            onChange={(e) => handleSearch(e.target.value)}
            className="pl-10"
          />
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {themas.map((thema) => (
            <div
              key={thema.id}
              className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
            >
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <h3 className="font-medium text-gray-900">{thema.display_name}</h3>
                  <Badge variant={thema.is_active ? "default" : "secondary"}>
                    {thema.is_active ? 'Actief' : 'Inactief'}
                  </Badge>
                  <Badge variant="outline" className="text-xs">
                    {thema.element_count} elementen
                  </Badge>
                </div>
                <p className="text-sm text-gray-600 mb-1">{thema.description}</p>
                <p className="text-xs text-gray-400">
                  Aangemaakt: {new Date(thema.created_at).toLocaleDateString('nl-NL')}
                </p>
              </div>
              
              <div className="flex items-center gap-2">
                                <AlertDialog open={selectedThemaId !== null} onOpenChange={(open) => !open && handleCloseDialog()}>
                  <AlertDialogTrigger asChild>
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleView(thema)}
                      className="text-blue-600 hover:text-blue-800 hover:bg-blue-50"
                    >
                      <EyeIcon className="h-4 w-4" />
                    </Button>
                  </AlertDialogTrigger>
                  <AlertDialogContent className="max-w-6xl max-h-[90vh] overflow-y-auto">
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        {selectedThemaId && themaDetails ? themaDetails.display_name : 'Thema Details'}
                      </AlertDialogTitle>
                      <AlertDialogDescription asChild>
                        <div>
                          {detailsLoading ? (
                            <div className="space-y-2">
                              <Skeleton className="h-4 w-full" />
                              <Skeleton className="h-4 w-3/4" />
                            </div>
                          ) : selectedThemaId && themaDetails ? (
                            <div className="space-y-4">
                              <p className="text-gray-600">{themaDetails.description}</p>
                              
                              <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as 'elements' | 'prompt')}>
                                <TabsList className="grid w-full grid-cols-2">
                                  <TabsTrigger value="elements">🎵 Elementen</TabsTrigger>
                                  <TabsTrigger value="prompt">📝 Professionele Prompt</TabsTrigger>
                                </TabsList>
                                
                                <TabsContent value="elements" className="mt-4">
                                  <ThemaElementsEditor
                                    themaId={selectedThemaId}
                                    elements={elements || []}
                                    isEditing={editingElementsId === selectedThemaId}
                                    onToggleEdit={handleToggleElementsEdit}
                                    onElementsChange={refetchThemaDetails}
                                  />
                                </TabsContent>
                                
                                <TabsContent value="prompt" className="mt-4">
                                  <ProfessionalPromptEditor
                                    thema={themaDetails}
                                    isEditing={editingPromptId === selectedThemaId}
                                    onToggleEdit={handleTogglePromptEdit}
                                    onPromptUpdated={refetchThemaDetails}
                                  />
                                </TabsContent>
                              </Tabs>
                            </div>
                          ) : (
                            <p>Geen thema geselecteerd</p>
                          )}
                        </div>
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogAction onClick={handleCloseDialog}>Sluiten</AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
                
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleEdit(thema)}
                  className="text-green-600 hover:text-green-800 hover:bg-green-50"
                >
                  <EditIcon className="h-4 w-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleDelete(thema)}
                  className="text-red-600 hover:text-red-800 hover:bg-red-50"
                >
                  <TrashIcon className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
          
          {themas.length === 0 && (
            <div className="text-center py-8">
              <p className="text-gray-500">Geen thema's gevonden</p>
              <p className="text-sm text-gray-400 mt-1">
                Probeer een andere zoekterm of maak een nieuw thema aan
              </p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default ThemaList;
