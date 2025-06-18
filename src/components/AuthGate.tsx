
import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { XIcon } from '@/components/icons/IconComponents';
import { useToast } from '@/hooks/use-toast';

const AuthGate = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const { toast } = useToast();

  const handleLogin = () => {
    if (apiKey.trim() === 'jouwsong2025') {
      setIsAuthenticated(true);
      toast({
        title: "Succesvol ingelogd",
        description: "Welkom bij JouwSong Dashboard",
      });
    } else {
      toast({
        title: "Fout",
        description: "Ongeldige API sleutel",
        variant: "destructive",
      });
    }
  };

  if (isAuthenticated) {
    return <>{children}</>;
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full">
        <h1 className="text-2xl font-bold mb-6 text-center">JouwSong Dashboard</h1>
        <div className="space-y-4">
          <input
            type="password"
            placeholder="API Sleutel"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            className="w-full p-3 border rounded-lg"
            onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
          />
          <Button onClick={handleLogin} className="w-full">
            Inloggen
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AuthGate;
