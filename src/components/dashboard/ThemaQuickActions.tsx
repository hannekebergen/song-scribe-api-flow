
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PlusIcon, UploadIcon, DownloadIcon } from '@/components/icons/IconComponents';
import { useThemaCRUD } from '@/hooks/useThema';

const ThemaQuickActions = () => {
  const { createThema } = useThemaCRUD();

  const handleNewThema = async () => {
    const name = prompt('Voer de naam in voor het nieuwe thema (bijv. "kerst_viering"):');
    if (!name) return;
    
    const displayName = prompt('Voer de weergavenaam in (bijv. "Kerst Viering"):');
    if (!displayName) return;
    
    const description = prompt('Voer een beschrijving in (optioneel):') || undefined;
    
    try {
      await createThema({
        name: name.toLowerCase().replace(/\s+/g, '_'),
        display_name: displayName,
        description,
        is_active: true
      });
      // Refresh the page to show the new thema
      window.location.reload();
    } catch (error) {
      console.error('Error creating thema:', error);
    }
  };

  const handleImportCSV = () => {
    // TODO: Implement CSV import
    alert('CSV import functionaliteit wordt binnenkort toegevoegd');
  };

  const handleExportData = () => {
    // TODO: Implement data export  
    alert('Export functionaliteit wordt binnenkort toegevoegd');
  };

  const handleEditPrompts = () => {
    alert('💡 Tip: Klik op het 👁️ oog-icoon bij een thema en ga naar de "Professionele Prompt" tab om prompts te bewerken!');
  };

  return (
    <Card className="bg-gradient-to-br from-green-50 to-emerald-100 border-green-200">
      <CardContent className="p-6">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-green-800">Thema Beheer</h3>
          <span className="text-2xl">🎵</span>
        </div>
        <div className="space-y-3">
          <Button 
            onClick={handleNewThema}
            className="w-full bg-green-600 hover:bg-green-700 text-white"
          >
            <PlusIcon className="h-4 w-4 mr-2" />
            Nieuw Thema
          </Button>
          <Button 
            onClick={handleEditPrompts}
            variant="outline" 
            className="w-full border-purple-300 text-purple-700 hover:bg-purple-50"
          >
            📝 Bewerk Prompts
          </Button>
          <Button 
            onClick={handleImportCSV}
            variant="outline" 
            className="w-full border-green-300 text-green-700 hover:bg-green-50"
          >
            <UploadIcon className="h-4 w-4 mr-2" />
            Import CSV
          </Button>
          <Button 
            onClick={handleExportData}
            variant="outline" 
            className="w-full border-green-300 text-green-700 hover:bg-green-50"
          >
            <DownloadIcon className="h-4 w-4 mr-2" />
            Export Data
          </Button>
        </div>
        <div className="mt-4 pt-4 border-t border-green-200">
          <p className="text-sm text-green-600">
            Beheer je thema database en elementen voor AI prompt generatie.
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default ThemaQuickActions;
