
import { Toaster } from "@/components/ui/toaster";
import { Toaster as Sonner } from "@/components/ui/sonner";
import { TooltipProvider } from "@/components/ui/tooltip";
import useKeepAlive from "@/hooks/useKeepAlive";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import AuthGate from "./components/AuthGate";
import Index from "./pages/Index";
import NotFound from "./pages/NotFound";
import Dashboard from "./components/Dashboard";
import OrderDetail from "./components/OrderDetail";
import OrdersList from "./components/OrdersList";

const queryClient = new QueryClient();

const App = () => {
  useKeepAlive(); // houdt Render wakker
  
  return (
  <QueryClientProvider client={queryClient}>
    <TooltipProvider>
      <Toaster />
      <Sonner />
      <AuthGate>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Index />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/orders/:id" element={<OrderDetail />} />
            <Route path="/orders" element={
              <div className="container mx-auto p-6 space-y-6">
                <h1 className="text-3xl font-bold">Lijst van bestellingen</h1>
                <OrdersList />
              </div>
            } />
            {/* ADD ALL CUSTOM ROUTES ABOVE THE CATCH-ALL "*" ROUTE */}
            <Route path="*" element={<NotFound />} />
          </Routes>
        </BrowserRouter>
      </AuthGate>
    </TooltipProvider>
  </QueryClientProvider>
  );
};

export default App;
