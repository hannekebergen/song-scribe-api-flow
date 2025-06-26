
import React, { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { SearchIcon, EditIcon, TrashIcon, EyeIcon } from '@/components/icons/IconComponents';

interface MockThema {
  id: number;
  name: string;
  display_name: string;
  description: string;
  is_active: boolean;
  element_count: number;
  created_at: string;
}

const ThemaList = () => {
  const [searchTerm, setSearchTerm] = useState('');
  
  // Mock data - will be replaced with real API data
  const mockThemas: MockThema[] = [
    {
      id: 1,
      name: 'verjaardag',
      display_name: 'Verjaardag',
      description: 'Thema voor verjaardagsliedjes met vrolijke en feestelijke elementen',
      is_active: true,
      element_count: 24,
      created_at: '2025-01-15'
    },
    {
      id: 2,
      name: 'liefde',
      display_name: 'Liefde',
      description: 'Romantische thema voor liefdesliedjes en relaties',
      is_active: true,
      element_count: 32,
      created_at: '2025-01-12'
    },
    {
      id: 3,
      name: 'huwelijk',
      display_name: 'Huwelijk',
      description: 'Thema voor bruiloften en huwelijksfeesten',
      is_active: true,
      element_count: 18,
      created_at: '2025-01-10'
    },
    {
      id: 4,
      name: 'afscheid',
      display_name: 'Afscheid',
      description: 'Thema voor afscheidsliedjes en herinneringen',
      is_active: false,
      element_count: 15,
      created_at: '2025-01-08'
    }
  ];

  const filteredThemas = mockThemas.filter(thema =>
    thema.display_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    thema.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handleEdit = (thema: MockThema) => {
    console.log('Edit thema:', thema.name);
    // TODO: Implement edit functionality
  };

  const handleView = (thema: MockThema) => {
    console.log('View thema:', thema.name);
    // TODO: Implement view functionality
  };

  const handleDelete = (thema: MockThema) => {
    console.log('Delete thema:', thema.name);
    // TODO: Implement delete functionality
  };

  return (
    <Card className="bg-white shadow-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-xl font-semibold text-gray-800">
            Thema Overzicht
          </CardTitle>
          <Badge variant="secondary" className="bg-blue-100 text-blue-800">
            {filteredThemas.length} thema's
          </Badge>
        </div>
        
        {/* Search */}
        <div className="relative">
          <SearchIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Zoek thema's..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>
      </CardHeader>
      
      <CardContent>
        <div className="space-y-4">
          {filteredThemas.map((thema) => (
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
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => handleView(thema)}
                  className="text-blue-600 hover:text-blue-800 hover:bg-blue-50"
                >
                  <EyeIcon className="h-4 w-4" />
                </Button>
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
          
          {filteredThemas.length === 0 && (
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
