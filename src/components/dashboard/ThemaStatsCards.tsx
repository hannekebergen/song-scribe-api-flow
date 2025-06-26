
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';
import { useThemaStats } from '@/hooks/useThema';

const ThemaStatsCards = () => {
  const { stats, loading, error } = useThemaStats();

  if (loading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <Card key={i} className="bg-gradient-to-br from-gray-50 to-gray-100">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <Skeleton className="h-4 w-24 mb-2" />
                  <Skeleton className="h-8 w-16" />
                </div>
                <Skeleton className="h-12 w-12 rounded-lg" />
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    );
  }

  if (error || !stats) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card className="bg-gradient-to-br from-red-50 to-red-100 border-red-200">
          <CardContent className="p-6">
            <p className="text-sm text-red-600">
              {error || 'Geen statistieken beschikbaar'}
            </p>
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      {/* Total Themas */}
      <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-blue-600 text-sm font-medium">Totaal Thema's</p>
              <p className="text-2xl font-bold text-blue-800">{stats.total_themas}</p>
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
              <p className="text-2xl font-bold text-green-800">{stats.active_themas}</p>
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
              <p className="text-2xl font-bold text-purple-800">{stats.total_elements}</p>
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
              <p className="text-2xl font-bold text-orange-800">{stats.recent_additions}</p>
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
