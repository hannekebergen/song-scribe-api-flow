
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Button } from '@/components/ui/button';
import { FilterIcon, SearchIcon } from '@/components/icons/IconComponents';

interface FiltersSectionProps {
  searchTerm: string;
  setSearchTerm: (term: string) => void;
  themaFilter: string;
  setThemaFilter: (thema: string) => void;
  statusFilter: string;
  setStatusFilter: (status: string) => void;
  uniqueThemas: string[];
}

const FiltersSection: React.FC<FiltersSectionProps> = ({
  searchTerm,
  setSearchTerm,
  themaFilter,
  setThemaFilter,
  statusFilter,
  setStatusFilter,
  uniqueThemas
}) => {
  const handleReset = () => {
    setSearchTerm('');
    setThemaFilter('all');
    setStatusFilter('all');
  };

  return (
    <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <FilterIcon className="h-5 w-5 text-blue-600" />
          Filters & Zoeken
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Zoek op klantnaam</label>
            <div className="relative">
              <SearchIcon className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
              <Input
                placeholder="Klantnaam..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-10 border-gray-200 focus:border-blue-500 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Thema</label>
            <Select value={themaFilter} onValueChange={setThemaFilter}>
              <SelectTrigger 
                aria-label="Open selectie voor thema" 
                className="border-gray-200 focus:border-blue-500 focus:ring-blue-500"
              >
                <SelectValue placeholder="Alle thema's" />
                <span className="sr-only">Open dropdown voor thema selectie</span>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Alle themas</SelectItem>
                {uniqueThemas.map(thema => (
                  <SelectItem key={thema} value={thema}>{thema}</SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Status</label>
            <Select value={statusFilter} onValueChange={setStatusFilter}>
              <SelectTrigger 
                aria-label="Open selectie voor status" 
                className="border-gray-200 focus:border-blue-500 focus:ring-blue-500"
              >
                <SelectValue placeholder="Alle statussen" />
                <span className="sr-only">Open dropdown voor status selectie</span>
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="all">Alle statussen</SelectItem>
                <SelectItem value="nieuw">Nieuw</SelectItem>
                <SelectItem value="gegenereerd">Gegenereerd</SelectItem>
              </SelectContent>
            </Select>
          </div>

          <div className="space-y-2">
            <label className="text-sm font-semibold text-gray-700">Acties</label>
            <Button
              variant="outline"
              onClick={handleReset}
              className="w-full border-gray-200 hover:bg-gray-50"
            >
              Reset filters
            </Button>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default FiltersSection;
