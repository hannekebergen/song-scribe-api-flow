
import React from 'react';
import ThemaStatsCards from './ThemaStatsCards';
import ThemaQuickActions from './ThemaQuickActions';
import ThemaList from './ThemaList';

const ThemaManagement = () => {
  return (
    <div className="space-y-8">
      {/* Stats cards for themes */}
      <ThemaStatsCards />
      
      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        {/* Quick actions */}
        <div className="lg:col-span-1">
          <ThemaQuickActions />
        </div>
        
        {/* Thema list with management */}
        <div className="lg:col-span-3">
          <ThemaList />
        </div>
      </div>
    </div>
  );
};

export default ThemaManagement;
