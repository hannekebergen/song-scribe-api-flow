import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Skeleton } from '@/components/ui/skeleton';
import { AlertDialog, AlertDialogAction, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from '@/components/ui/alert-dialog';
import { SearchIcon, EditIcon, TrashIcon, EyeIcon } from '@/components/icons/IconComponents';
import { useThemas, useThemaCRUD, useThemaDetails } from '@/hooks/useThema';
import { Thema, ThemaElement } from '@/services/themaApi';

// Helper component for displaying elements list with expand functionality
const ElementsList: React.FC<{ elements: ThemaElement[] }> = ({ elements }) => {
  const [showAll, setShowAll] = useState(false);
  const displayElements = showAll ? elements : elements.slice(0, 12);

  return (
    <div className="space-y-2">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2">
        {displayElements.map((element, idx) => (
          <div key={idx} className="bg-gray-50 p-2 rounded text-xs">
            <span className="font-medium text-blue-600">{element.element_type}:</span> {element.content}
          </div>
        ))}
      </div>
      {elements.length > 12 && (
        <div className="text-center">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowAll(!showAll)}
            className="text-xs text-gray-500 hover:text-gray-700 hover:bg-gray-100"
          >
            {showAll ? 'Toon minder' : `+${elements.length - 12} meer...`}
          </Button>
        </div>
      )}
    </div>
  );
};

const ThemaList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedThemaId, setSelectedThemaId] = useState<number | null>(null);
  const { themas, loading, error, updateParams } = useThemas();
  const { deleteThema, loading: crudLoading } = useThemaCRUD();
  const { thema: themaDetails, elements, rhymeSets, loading: detailsLoading } = useThemaDetails(selectedThemaId);

  const handleSearch = (value: string) => {
    setSearchTerm(value);
    updateParams({ search: value || undefined });
  };

  const handleEdit = (thema: Thema) => {
    console.log('Edit thema:', thema.name);
    // TODO: Implement edit functionality
    alert(`Edit functionaliteit wordt binnenkort toegevoegd voor: ${thema.display_name}`);
  };

  const handleView = (thema: Thema) => {
    setSelectedThemaId(thema.id);
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
                <AlertDialog>
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
                  <AlertDialogContent className="max-w-4xl max-h-[80vh] overflow-y-auto">
                    <AlertDialogHeader>
                      <AlertDialogTitle>
                        {selectedThemaId && themaDetails ? themaDetails.display_name : 'Thema Details'}
                      </AlertDialogTitle>
                      <AlertDialogDescription>
                        {detailsLoading ? (
                          <div className="space-y-2">
                            <Skeleton className="h-4 w-full" />
                            <Skeleton className="h-4 w-3/4" />
                          </div>
                        ) : selectedThemaId && themaDetails ? (
                                                      <div className="space-y-4">
                             <p>{themaDetails.description}</p>
                             
                             <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                               <div>
                                 <h4 className="font-semibold mb-2">Basis Info</h4>
                                 <div className="space-y-1 text-sm">
                                   <p><strong>Naam:</strong> {themaDetails.name}</p>
                                   <p><strong>Status:</strong> {themaDetails.is_active ? '🟢 Actief' : '🔴 Inactief'}</p>
                                   <p><strong>Elementen:</strong> {elements?.length || 0}</p>
                                   <p><strong>Rijmsets:</strong> {rhymeSets?.length || 0}</p>
                                 </div>
                               </div>
                               
                               {elements && elements.length > 0 && (
                                 <div>
                                   <h4 className="font-semibold mb-2">Element Types</h4>
                                   <div className="space-y-1 text-sm">
                                     {Object.entries(
                                       elements.reduce((acc, el) => {
                                         acc[el.element_type] = (acc[el.element_type] || 0) + 1;
                                         return acc;
                                       }, {} as Record<string, number>)
                                     ).map(([type, count]) => (
                                       <p key={type}>
                                         <strong>{type}:</strong> {count} stuks
                                       </p>
                                     ))}
                                   </div>
                                 </div>
                               )}
                             </div>
                             
                             {elements && elements.length > 0 && (
                               <div>
                                 <h4 className="font-semibold mb-2">Voorbeeld Elementen</h4>
                                 <ElementsList elements={elements} />
                               </div>
                             )}
                          </div>
                        ) : (
                          <p>Geen thema geselecteerd</p>
                        )}
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogAction>Sluiten</AlertDialogAction>
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
