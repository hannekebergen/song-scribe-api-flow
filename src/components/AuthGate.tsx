
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { XIcon } from '@/components/icons/IconComponents';
import { useToast } from '@/hooks/use-toast';

const AuthGate = ({ children }: { children: React.ReactNode }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [apiKey, setApiKey] = useState('');
  const [isLoading, setIsLoading] = useState(true);
  const { toast } = useToast();

  // Check localStorage on component mount
  useEffect(() => {
    const savedAuth = localStorage.getItem('jouwsong_auth');
    if (savedAuth === 'authenticated') {
      setIsAuthenticated(true);
    }
    setIsLoading(false);
  }, []);

  const handleLogin = () => {
    if (apiKey.trim() === 'jouwsong2025') {
      setIsAuthenticated(true);
      localStorage.setItem('jouwsong_auth', 'authenticated');
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

  const handleLogout = () => {
    setIsAuthenticated(false);
    localStorage.removeItem('jouwsong_auth');
    toast({
      title: "Uitgelogd",
      description: "Je bent succesvol uitgelogd",
    });
  };

  // Show loading state during initial auth check
  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="bg-white p-8 rounded-lg shadow-lg max-w-md w-full text-center">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Laden...</p>
        </div>
      </div>
    );
  }

  if (isAuthenticated) {
    return (
      <div className="min-h-screen">
        {/* Logout button in top right */}
        <div className="fixed top-4 right-4 z-50">
          <Button 
            onClick={handleLogout}
            variant="outline"
            size="sm"
            className="bg-white/80 backdrop-blur-sm hover:bg-white/90"
          >
            Uitloggen
          </Button>
        </div>
        {children}
      </div>
    );
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
