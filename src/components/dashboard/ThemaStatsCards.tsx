
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';

const ThemaStatsCards = () => {
  // Mock data for now - will be replaced with real data from API
  const stats = {
    totalThemas: 12,
    activeThemas: 10,
    totalElements: 156,
    recentlyAdded: 3
  };

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* Total Themas */}
      <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-600 text-sm font-medium">Totaal Thema's</p>
              <p className="text-2xl font-bold text-blue-800">{stats.totalThemas}</p>
            </div>
            <div className="h-12 w-12 bg-blue-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">🎵</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Active Themas */}
      <Card className="bg-gradient-to-br from-green-50 to-green-100 border-green-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-green-600 text-sm font-medium">Actieve Thema's</p>
              <p className="text-2xl font-bold text-green-800">{stats.activeThemas}</p>
            </div>
            <div className="h-12 w-12 bg-green-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">✅</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Total Elements */}
      <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-purple-600 text-sm font-medium">Totaal Elementen</p>
              <p className="text-2xl font-bold text-purple-800">{stats.totalElements}</p>
            </div>
            <div className="h-12 w-12 bg-purple-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">🏷️</span>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Recently Added */}
      <Card className="bg-gradient-to-br from-orange-50 to-orange-100 border-orange-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-orange-600 text-sm font-medium">Recent Toegevoegd</p>
              <p className="text-2xl font-bold text-orange-800">{stats.recentlyAdded}</p>
            </div>
            <div className="h-12 w-12 bg-orange-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-xl">🆕</span>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ThemaStatsCards;
