
import React from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { BarChartIcon, ClockIcon, UsersIcon, TrendingUpIcon } from '@/components/icons/IconComponents';
import { MappedOrder } from '@/hooks/useFetchOrders';

interface StatsCardsProps {
  mappedOrders: MappedOrder[];
}

const StatsCards: React.FC<StatsCardsProps> = ({ mappedOrders }) => {
  const getStats = () => {
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    const spoedOrders = safeOrders.filter(order => order.deadline && order.deadline.includes('uur')).length;
    const uniqueThemas = [...new Set(safeOrders.map(order => order.thema))].length;
    const recentOrders = safeOrders.filter(order => {
      const orderDate = new Date(order.originalOrder.bestel_datum);
      const today = new Date();
      const diffTime = Math.abs(today.getTime() - orderDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays <= 7;
    }).length;

    return { spoedOrders, uniqueThemas, recentOrders };
  };

  const stats = getStats();

  return (
    <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
      <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-500 to-blue-600 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-blue-100 text-sm font-medium">Totaal Orders</p>
              <p className="text-3xl font-bold">{mappedOrders?.length || 0}</p>
            </div>
            <div className="h-12 w-12 bg-blue-400 bg-opacity-30 rounded-full flex items-center justify-center">
              <BarChartIcon className="h-6 w-6" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-lg bg-gradient-to-br from-orange-500 to-red-500 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-orange-100 text-sm font-medium">Spoed Orders</p>
              <p className="text-3xl font-bold">{stats.spoedOrders}</p>
            </div>
            <div className="h-12 w-12 bg-orange-400 bg-opacity-30 rounded-full flex items-center justify-center">
              <ClockIcon className="h-6 w-6" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-lg bg-gradient-to-br from-green-500 to-emerald-500 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-green-100 text-sm font-medium">Unieke Themas</p>
              <p className="text-3xl font-bold">{stats.uniqueThemas}</p>
            </div>
            <div className="h-12 w-12 bg-green-400 bg-opacity-30 rounded-full flex items-center justify-center">
              <UsersIcon className="h-6 w-6" />
            </div>
          </div>
        </CardContent>
      </Card>

      <Card className="border-0 shadow-lg bg-gradient-to-br from-purple-500 to-indigo-500 text-white">
        <CardContent className="p-6">
          <div className="flex items-center justify-between">
            <div className="space-y-1">
              <p className="text-purple-100 text-sm font-medium">Deze Week</p>
              <p className="text-3xl font-bold">{stats.recentOrders}</p>
            </div>
            <div className="h-12 w-12 bg-purple-400 bg-opacity-30 rounded-full flex items-center justify-center">
              <TrendingUpIcon className="h-6 w-6" />
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default StatsCards;
