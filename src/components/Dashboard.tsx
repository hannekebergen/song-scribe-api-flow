import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Search, Filter, Eye } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { useFetchOrders, MappedOrder } from '../hooks/useFetchOrders';
import FetchOrdersCard from './FetchOrdersCard';

const Dashboard = () => {
  // Gebruik de useFetchOrders hook in plaats van direct ordersApi aan te roepen
  const { mappedOrders, loading: ordersLoading, fetchOrders } = useFetchOrders();
  const [filteredOrders, setFilteredOrders] = useState<MappedOrder[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [themaFilter, setThemaFilter] = useState('all');
  const [statusFilter, setStatusFilter] = useState('all');

  useEffect(() => {
    // Haal orders op bij het laden van de component
    fetchOrders();
  }, []);

  useEffect(() => {
    filterOrders();
  }, [mappedOrders, searchTerm, themaFilter, statusFilter]);

  const filterOrders = () => {
    // Zorg ervoor dat we altijd met een array werken, zelfs als mappedOrders undefined is
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    let filtered = safeOrders;

    // Zoek op klantnaam
    if (searchTerm) {
      filtered = filtered.filter(order =>
        order.klant.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    // Filter op thema
    if (themaFilter !== 'all') {
      filtered = filtered.filter(order => order.thema === themaFilter);
    }

    // Filter op status (niet beschikbaar in mappedOrders, dus overslaan)
    // We kunnen later status toevoegen aan de MappedOrder interface indien nodig

    setFilteredOrders(filtered);
  };

  const getStatusBadge = (deadline: string) => {
    // Gebruik deadline als indicator voor urgentie/status
    return deadline.includes('uur') ? (
      <Badge variant="outline">Spoed</Badge>
    ) : (
      <Badge variant="default">Standaard</Badge>
    );
  };

  const getUniqueThemas = () => {
    // Zorg ervoor dat we altijd met een array werken
    const safeOrders = Array.isArray(mappedOrders) ? mappedOrders : [];
    return [...new Set(safeOrders.map(order => order.thema))];
  };

  if (ordersLoading) {
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
          {filteredOrders.length} van {mappedOrders?.length || 0} orders
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
                  <label className="text-sm font-medium">Zoek op klantnaam</label>
                  <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                    <Input
                      placeholder="Klantnaam..."
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
                <TableHead>Klant</TableHead>
                <TableHead>Deadline</TableHead>
                <TableHead>Acties</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {filteredOrders.map((order) => (
                <TableRow key={order.originalOrder.id}>
                  <TableCell className="font-mono">{order.ordernummer}</TableCell>
                  <TableCell>{order.datum}</TableCell>
                  <TableCell>
                    <Badge variant="secondary">{order.thema}</Badge>
                  </TableCell>
                  <TableCell className="font-medium">{order.klant}</TableCell>
                  <TableCell>{getStatusBadge(order.deadline)}</TableCell>
                  <TableCell>
                    <Button asChild variant="outline" size="sm">
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
