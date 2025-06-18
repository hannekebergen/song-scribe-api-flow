
import React from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { UserIcon, CalendarIcon } from '@/components/icons/IconComponents';
import { Order } from '@/types';

interface PersonalInfoCardProps {
  order: Order;
}

const PersonalInfoCard: React.FC<PersonalInfoCardProps> = ({ order }) => {
  return (
    <Card className="border-0 shadow-lg bg-white/90 backdrop-blur-sm">
      <CardHeader className="pb-4">
        <CardTitle className="flex items-center gap-2 text-gray-800">
          <UserIcon className="h-5 w-5 text-blue-600" />
          Persoonlijke Gegevens
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Voornaam</label>
            <div className="text-lg font-medium text-gray-800">{order.voornaam || '-'}</div>
          </div>
          <div className="space-y-1">
            <label className="text-sm font-semibold text-gray-600">Besteldatum</label>
            <div className="flex items-center gap-2 text-lg font-medium text-gray-800">
              <CalendarIcon className="h-4 w-4 text-blue-600" />
              {new Date(order.bestel_datum).toLocaleDateString('nl-NL', {
                weekday: 'long',
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  );
};

export default PersonalInfoCard;
