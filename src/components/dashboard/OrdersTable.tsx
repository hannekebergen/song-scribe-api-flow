import React from 'react';
import { Link } from 'react-router-dom';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { EyeIcon, SearchIcon } from '@/components/icons/IconComponents';
import { MappedOrder } from '@/hooks/useFetchOrders';
import { getOrderTypeBadge, isSpeedOrder } from '@/utils/orderTypeDetection';

interface OrdersTableProps {
  filteredOrders: MappedOrder[];
}

const OrdersTable: React.FC<OrdersTableProps> = ({ filteredOrders }) => {
  const getTypeOrderBadge = (order: MappedOrder) => {
    const badgeType = getOrderTypeBadge(order.originalOrder);
    const isSpoed = isSpeedOrder(order.originalOrder);
    
    switch (badgeType) {
      case 'spoed':
        return (
          <Badge variant="destructive" className="font-medium">
            🚀 Spoed 24u
          </Badge>
        );
      case 'standaard':
        return (
          <Badge variant="secondary" className="font-medium bg-blue-100 text-blue-800">
            📝 Standaard 72u
          </Badge>
        );
      case 'upsell':
        return (
          <Badge variant="outline" className="font-medium bg-purple-100 text-purple-800 border-purple-200">
            ⬆️ Upsell
          </Badge>
        );
      case 'order-bump':
        return (
          <Badge variant="outline" className="font-medium bg-green-100 text-green-800 border-green-200">
            ➕ Add-on
          </Badge>
        );
      default:
        return (
          <Badge variant="secondary" className="font-medium bg-gray-100 text-gray-800">
            ❓ Onbekend
          </Badge>
        );
    }
  };

  const getPromptStatusBadge = (order: MappedOrder) => {
    const hasPrompt = order.originalOrder.songtekst && order.originalOrder.songtekst.trim().length > 0;
    
    return hasPrompt ? (
      <Badge variant="default" className="font-medium bg-green-100 text-green-800 border-green-200">
        🖋️ Prompt gereed
      </Badge>
    ) : (
      <Badge variant="outline" className="font-medium text-gray-600 border-gray-300">
        Prompt ontbreekt
      </Badge>
    );
  };

  return (
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
                <TableHead className="font-semibold text-gray-700">Type Order</TableHead>
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
                  <TableCell>
                    <div className="flex flex-col gap-1">
                      {getTypeOrderBadge(order)}
                      {order.typeOrder !== 'Standaard 72u' && order.typeOrder !== 'Spoed 24u' && (
                        <span className="text-xs text-gray-500">{order.typeOrder}</span>
                      )}
                    </div>
                  </TableCell>
                  <TableCell className="text-gray-600">{order.datum}</TableCell>
                  <TableCell>
                    <Badge variant="secondary" className="bg-blue-100 text-blue-800 font-medium">
                      {order.thema}
                    </Badge>
                  </TableCell>
                  <TableCell className="font-medium text-gray-800">{order.klant}</TableCell>
                  <TableCell>{getPromptStatusBadge(order)}</TableCell>
                  <TableCell>
                    <Button asChild variant="outline" size="sm" className="border-blue-200 text-blue-600 hover:bg-blue-50 hover:border-blue-300">
                      <Link to={`/orders/${order.ordernummer}`}>
                        <EyeIcon className="h-4 w-4 mr-2" />
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
                <SearchIcon className="h-12 w-12 mx-auto text-gray-300" />
              </div>
              <p className="text-lg font-medium">Geen orders gevonden</p>
              <p className="text-sm">Probeer je zoekfilters aan te passen</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default OrdersTable;
