
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Eye, BarChart3, Clock, Users, TrendingUp } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useFetchOrders, MappedOrder } from '../hooks/useFetchOrders';
import FetchOrdersCard from './FetchOrdersCard';

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

  const getStatusBadge = (deadline: string) => {
    return deadline.includes('uur') ? (
      <Badge variant="destructive" className="font-medium">Spoed</Badge>
    ) : (
      <Badge variant="secondary" className="font-medium">Standaard</Badge>
    );
  };

  const getUniqueThemas = () => {
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    return [...new Set(safeOrders.map(order => order.thema))];
  };

  const getStats = () => {
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    const spoedOrders = safeOrders.filter(order => order.deadline.includes('uur')).length;
    const uniqueThemas = getUniqueThemas().length;
    const recentOrders = safeOrders.filter(order => {
      const orderDate = new Date(order.originalOrder.bestel_datum);
      const today = new Date();
      const diffTime = Math.abs(today.getTime() - orderDate.getTime());
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return diffDays <= 7;
    }).length;

    return { spoedOrders, uniqueThemas, recentOrders };
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

  const stats = getStats();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50">
      <div className="container mx-auto px-6 py-8 space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
              JouwSong Dashboard
            </h1>
            <p className="text-gray-600">Beheer je bestellingen en houd statistieken bij</p>
          </div>
          <div className="flex items-center space-x-2 text-sm text-gray-500 bg-white px-4 py-2 rounded-full shadow-sm border">
            <BarChart3 className="h-4 w-4" />
            <span className="font-medium">{filteredOrders.length} van {mappedOrders?.length || 0} orders</span>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="border-0 shadow-lg bg-gradient-to-br from-blue-500 to-blue-600 text-white">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div className="space-y-1">
                  <p className="text-blue-100 text-sm font-medium">Totaal Orders</p>
                  <p className="text-3xl font-bold">{mappedOrders?.length || 0}</p>
                </div>
                <div className="h-12 w-12 bg-blue-400 bg-opacity-30 rounded-full flex items-center justify-center">
                  <BarChart3 className="h-6 w-6" />
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
                  <Clock className="h-6 w-6" />
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
                  <Users className="h-6 w-6" />
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
                  <TrendingUp className="h-6 w-6" />
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Fetch Orders Card */}
          <div className="lg:col-span-1">
            <FetchOrdersCard />
          </div>
          
          {/* Filters */}
          <div className="lg:col-span-3">
            <Card className="border-0 shadow-lg bg-white/80 backdrop-blur-sm">
              <CardHeader className="pb-4">
                <CardTitle className="flex items-center gap-2 text-gray-800">
                  <Filter className="h-5 w-5 text-blue-600" />
                  Filters & Zoeken
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-gray-700">Zoek op klantnaam</label>
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
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
                      <SelectTrigger className="border-gray-200 focus:border-blue-500 focus:ring-blue-500">
                        <SelectValue placeholder="Alle themas" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="all">Alle themas</SelectItem>
                        {getUniqueThemas().map(thema => (
                          <SelectItem key={thema} value={thema}>{thema}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-semibold text-gray-700">Status</label>
                    <Select value={statusFilter} onValueChange={setStatusFilter}>
                      <SelectTrigger className="border-gray-200 focus:border-blue-500 focus:ring-blue-500">
                        <SelectValue placeholder="Alle statussen" />
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
                      onClick={() => {
                        setSearchTerm('');
                        setThemaFilter('all');
                        setStatusFilter('all');
                      }}
                      className="w-full border-gray-200 hover:bg-gray-50"
                    >
                      Reset filters
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Orders Table */}
        <Card className="border-0 shadow-xl bg-white/90 backdrop-blur-sm">
          <CardHeader className="pb-4">
            <CardTitle className="text-xl text-gray-800">
              Orders ({filteredOrders.length})
            </CardTitle>
          </CardHeader>
          <CardContent className="p-0">
            <div className="overflow-hidden">
              <Table>
                <TableHeader>
                  <TableRow className="bg-gray-50 border-b">
                    <TableHead className="font-semibold text-gray-700">Ordernummer</TableHead>
                    <TableHead className="font-semibold text-gray-700">Datum</TableHead>
                    <TableHead className="font-semibold text-gray-700">Thema</TableHead>
                    <TableHead className="font-semibold text-gray-700">Klant</TableHead>
                    <TableHead className="font-semibold text-gray-700">Status</TableHead>
                    <TableHead className="font-semibold text-gray-700">Acties</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {filteredOrders.map((order, index) => (
                    <TableRow key={order.originalOrder.id} className={`hover:bg-blue-50/50 transition-colors ${index % 2 === 0 ? 'bg-white' : 'bg-gray-50/30'}`}>
                      <TableCell className="font-mono text-sm font-medium text-blue-600">
                        #{order.ordernummer}
                      </TableCell>
                      <TableCell className="text-gray-600">{order.datum}</TableCell>
                      <TableCell>
                        <Badge variant="secondary" className="bg-blue-100 text-blue-800 font-medium">
                          {order.thema}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-medium text-gray-800">{order.klant}</TableCell>
                      <TableCell>{getStatusBadge(order.deadline)}</TableCell>
                      <TableCell>
                        <Button asChild variant="outline" size="sm" className="border-blue-200 text-blue-600 hover:bg-blue-50 hover:border-blue-300">
                          <Link to={`/orders/${order.ordernummer}`}>
                            <Eye className="h-4 w-4 mr-2" />
                            Bekijk
                          </Link>
                        </Button>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>

              {filteredOrders.length === 0 && (
                <div className="text-center py-12 text-gray-500">
                  <div className="mb-4">
                    <Search className="h-12 w-12 mx-auto text-gray-300" />
                  </div>
                  <p className="text-lg font-medium">Geen orders gevonden</p>
                  <p className="text-sm">Probeer je zoekfilters aan te passen</p>
                </div>
              )}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default Dashboard;
