
import React, { useState, useEffect } from 'react';
import { Card, CardContent } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { BarChartIcon } from '@/components/icons/IconComponents';
import { useFetchOrders, MappedOrder } from '../hooks/useFetchOrders';
import FetchOrdersCard from './FetchOrdersCard';
import StatsCards from './dashboard/StatsCards';
import FiltersSection from './dashboard/FiltersSection';
import OrdersTable from './dashboard/OrdersTable';
import ThemaManagement from './dashboard/ThemaManagement';

const Dashboard = () => {
  const { mappedOrders, loading: ordersLoading, fetchOrders } = useFetchOrders();
  const [filteredOrders, setFilteredOrders] = useState<MappedOrder[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [themaFilter, setThemaFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    fetchOrders();
  }, []);

  useEffect(() => {
    filterOrders();
  }, [mappedOrders, searchTerm, themaFilter, statusFilter]);

  const filterOrders = () => {
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    let filtered = safeOrders;

    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.klant.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (themaFilter !== 'all') {
      filtered = filtered.filter(order => order.thema === themaFilter);
    }

    setFilteredOrders(filtered);
  };

  const getUniqueThemas = () => {
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    return [...new Set(safeOrders.map(order => order.thema))];
  };

  if (ordersLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="flex flex-col items-center space-y-4">
          <div className="w-8 h-8 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
          <div className="text-lg font-medium text-gray-700">Orders laden...</div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              JouwSong Dashboard
            </h1>
            <p className="text-gray-600">Beheer je bestellingen en thema database</p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500 bg-white px-4 py-2 rounded-full shadow-sm border">
            <BarChartIcon className="h-4 w-4" />
            <span className="font-medium">{filteredOrders.length} van {mappedOrders?.length || 0} orders</span>
          </div>
        </div>

        {/* Tabbed Interface */}
        <Tabs defaultValue="orders" className="space-y-8">
          <TabsList className="grid w-full grid-cols-3 bg-white shadow-sm">
            <TabsTrigger value="orders" className="flex items-center gap-2">
              📦 Orders
            </TabsTrigger>
            <TabsTrigger value="thema" className="flex items-center gap-2">
              🎵 Thema's
            </TabsTrigger>
            <TabsTrigger value="analytics" className="flex items-center gap-2">
              📊 Analytics
            </TabsTrigger>
          </TabsList>

          <TabsContent value="orders" className="space-y-8">
            {/* Stats Cards */}
            <StatsCards mappedOrders={mappedOrders || []} />

            {/* Main Content */}
            <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
              {/* Fetch Orders Card */}
              <div className="lg:col-span-1">
                <FetchOrdersCard />
              </div>
              
              {/* Filters */}
              <div className="lg:col-span-3">
                <FiltersSection
                  searchTerm={searchTerm}
                  setSearchTerm={setSearchTerm}
                  themaFilter={themaFilter}
                  setThemaFilter={setThemaFilter}
                  statusFilter={statusFilter}
                  setStatusFilter={setStatusFilter}
                  uniqueThemas={getUniqueThemas()}
                />
              </div>
            </div>

            {/* Orders Table */}
            <OrdersTable filteredOrders={filteredOrders} />
          </TabsContent>

          <TabsContent value="thema" className="space-y-8">
            <ThemaManagement />
          </TabsContent>

          <TabsContent value="analytics" className="space-y-8">
            <Card className="bg-gradient-to-br from-purple-50 to-purple-100 border-purple-200">
              <CardContent className="p-12 text-center">
                <div className="space-y-4">
                  <div className="h-16 w-16 bg-purple-500 rounded-full flex items-center justify-center mx-auto">
                    <span className="text-2xl">📊</span>
                  </div>
                  <h3 className="text-xl font-semibold text-purple-800">Analytics komen binnenkort</h3>
                  <p className="text-purple-600">Gedetailleerde statistieken en rapporten over orders en thema's</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default Dashboard;
