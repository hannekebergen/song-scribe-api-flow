
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileTextIcon } from '@/components/icons/IconComponents';
import { Order } from '@/types';

interface DescriptionCardProps {
  order: Order;
}

const DescriptionCard: React.FC<DescriptionCardProps> = ({ order }) => {
  const isDescriptionLong = (description: string) => {
    return description && description.split('\n').length > 10;
  };

  return (
    <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <FileTextIcon className="h-5 w-5 text-green-600" />
          Beschrijving
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className={`bg-gray-50 p-4 rounded-lg ${isDescriptionLong(order.beschrijving || '') ? 'max-h-60 overflow-y-auto' : ''}`}>
          <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
            {order.beschrijving || 'Geen beschrijving beschikbaar.'}
          </p>
        </div>
      </CardContent>
    </Card>
  );
};

export default DescriptionCard;
