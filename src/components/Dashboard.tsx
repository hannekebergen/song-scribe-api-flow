import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Eye } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { ordersApi, Order } from '@/services/api';
import FetchOrdersCard from './FetchOrdersCard';

const Dashboard = () => {
  const [orders, setOrders] = useState<Order[]>([]);
  const [filteredOrders, setFilteredOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [themaFilter, setThemaFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    loadOrders();
  }, []);

  useEffect(() => {
    filterOrders();
  }, [orders, searchTerm, themaFilter, statusFilter]);

  const loadOrders = async () => {
    try {
      const data = await ordersApi.getOrders();
      setOrders(data);
    } catch (error) {
      console.error('Error loading orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const filterOrders = () => {
    let filtered = orders;

    // Zoek op voornaam
    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.voornaam.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter op thema
    if (themaFilter !== 'all') {
      filtered = filtered.filter(order => order.thema === themaFilter);
    }

    // Filter op status
    if (statusFilter !== 'all') {
      filtered = filtered.filter(order => order.status === statusFilter);
    }

    setFilteredOrders(filtered);
  };

  const getStatusBadge = (status: string) => {
    return status === 'nieuw' ? (
      <Badge variant="outline">Nieuw</Badge>
    ) : (
      <Badge variant="default">Gegenereerd</Badge>
    );
  };

  const getUniqueThemas = () => {
    return [...new Set(orders.map(order => order.thema))];
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-lg">Orders laden...</div>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold">JouwSong Dashboard</h1>
        <div className="text-sm text-muted-foreground">
          {filteredOrders.length} van {orders.length} orders
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        <div className="lg:col-span-1">
          <FetchOrdersCard />
        </div>
        
        <div className="lg:col-span-3">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Filter className="h-5 w-5" />
                Filters & Zoeken
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <label className="text-sm font-medium">Zoek op voornaam</label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Voornaam..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className="pl-10"
                    />
                  </div>
                </div>

                <div className="space-y-2">
                  <label className="text-sm font-medium">Thema</label>
                  <Select value={themaFilter} onValueChange={setThemaFilter}>
                    <SelectTrigger>
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
                  <label className="text-sm font-medium">Status</label>
                  <Select value={statusFilter} onValueChange={setStatusFilter}>
                    <SelectTrigger>
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
                  <label className="text-sm font-medium">Acties</label>
                  <Button
                    variant="outline"
                    onClick={() => {
                      setSearchTerm('');
                      setThemaFilter('all');
                      setStatusFilter('all');
                    }}
                    className="w-full"
                  >
                    Reset filters
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Orders ({filteredOrders.length})</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Ordernummer</TableHead>
                <TableHead>Datum</TableHead>
                <TableHead>Thema</TableHead>
                <TableHead>Voornaam</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Acties</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredOrders.map((order) => (
                <TableRow key={order.order_id}>
                  <TableCell className="font-mono">{order.order_id}</TableCell>
                  <TableCell>{new Date(order.datum).toLocaleDateString('nl-NL')}</TableCell>
                  <TableCell>
                    <Badge variant="secondary">{order.thema}</Badge>
                  </TableCell>
                  <TableCell className="font-medium">{order.voornaam}</TableCell>
                  <TableCell>{getStatusBadge(order.status)}</TableCell>
                  <TableCell>
                    <Button asChild variant="outline" size="sm">
                      <Link to={`/orders/${order.order_id}`}>
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
            <div className="text-center py-8 text-muted-foreground">
              Geen orders gevonden met de huidige filters.
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default Dashboard;
