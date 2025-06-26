
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PlusIcon, UploadIcon, DownloadIcon } from '@/components/icons/IconComponents';

const ThemaQuickActions = () => {
  const handleNewThema = () => {
    // TODO: Implement new thema creation
    console.log('Nieuw thema aanmaken');
  };

  const handleImportCSV = () => {
    // TODO: Implement CSV import
    console.log('CSV importeren');
  };

  const handleExportData = () => {
    // TODO: Implement data export
    console.log('Data exporteren');
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
