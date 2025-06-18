
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { MusicIcon } from '@/components/icons/IconComponents';
import { Order } from '@/types';

interface SongDetailsCardProps {
  order: Order;
}

const SongDetailsCard: React.FC<SongDetailsCardProps> = ({ order }) => {
  return (
    <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <MusicIcon className="h-5 w-5 text-blue-600" />
          Song Specificaties
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Thema</label>
            <Badge variant="secondary" className="bg-blue-100 text-blue-800 font-medium text-base px-3 py-1">
              {order.thema || '-'}
            </Badge>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Toon</label>
            <div className="text-lg font-medium text-gray-800">{order.toon || '-'}</div>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Structuur</label>
            <div className="text-lg font-medium text-gray-800">{order.structuur || '-'}</div>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Rijm</label>
            <div className="text-lg font-medium text-gray-800">{order.rijm || '-'}</div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default SongDetailsCard;
