import axios from 'axios';

// Mock data voor development - vervang later met echte API calls
const mockOrders = [
  {
    order_id: "202540",
    voornaam: "Femm",
    van_naam: "Diana",
    relatie: "tantezegger",
    thema: "Verjaardag",
    toon: "Vrolijk",
    beschrijving: "Ze wordt 1 jaar, ouders vroegen om een levensles cadeau...",
    structuur: "3 coupletten + refrein",
    rijm: "ABBA",
    status: "nieuw" as const,
    datum: "2024-01-15",
    songtekst: ""
  },
  {
    order_id: "202541",
    voornaam: "Mark",
    van_naam: "Sarah",
    relatie: "vriend",
    thema: "Liefde",
    toon: "Romantisch",
    beschrijving: "Voor onze 5-jarige relatie, hij houdt van gitaar spelen...",
    structuur: "2 coupletten + refrein",
    rijm: "AABB",
    status: "gegenereerd" as const,
    datum: "2024-01-14",
    songtekst: "In de avond als de sterren schijnen helder\nDenk ik aan jou, mijn allerliefste kelder..."
  },
  {
    order_id: "202542",
    voornaam: "Lisa",
    van_naam: "Tom",
    relatie: "dochter",
    thema: "Verjaardag",
    toon: "Speels",
    beschrijving: "Ze wordt 8 jaar en houdt van paarden en tekenen...",
    structuur: "3 coupletten + refrein",
    rijm: "ABAB",
    status: "gegenereerd" as const,
    datum: "2024-01-13",
    songtekst: "Kleine Lisa wordt vandaag acht jaar\nMet haar penselen en haar krullen haar..."
  }
];

export interface Order {
  order_id: string;
  voornaam: string;
  van_naam: string;
  relatie: string;
  thema: string;
  toon: string;
  beschrijving: string;
  structuur: string;
  rijm: string;
  status: 'nieuw' | 'gegenereerd';
  datum: string;
  songtekst: string;
}

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const ordersApi = {
  // GET /api/orders - lijst van orders
  getOrders: async (): Promise<Order[]> => {
    try {
      // Voor nu mock data - vervang met echte API call
      // const response = await api.get('/api/orders');
      // return response.data;
      return mockOrders;
    } catch (error) {
      console.error('Error fetching orders:', error);
      return mockOrders; // Fallback naar mock data
    }
  },

  // GET /api/orders/:id - order details
  getOrder: async (orderId: string): Promise<Order | null> => {
    try {
      // const response = await api.get(`/api/orders/${orderId}`);
      // return response.data;
      return mockOrders.find(order => order.order_id === orderId) || null;
    } catch (error) {
      console.error('Error fetching order:', error);
      return null;
    }
  },

  // POST /api/orders/:id/regenerate - hergenereer prompt
  regeneratePrompt: async (orderId: string): Promise<Order | null> => {
    try {
      // const response = await api.post(`/api/orders/${orderId}/regenerate`);
      // return response.data;
      
      // Mock regeneration
      const order = mockOrders.find(o => o.order_id === orderId);
      if (order) {
        order.status = 'gegenereerd';
        order.songtekst = `Nieuwe gegenereerde songtekst voor ${order.voornaam}...\n(Gegenereerd op ${new Date().toLocaleString()})`;
      }
      return order || null;
    } catch (error) {
      console.error('Error regenerating prompt:', error);
      return null;
    }
  },

  // PATCH /api/orders/:id - update songtekst
  updateSongtext: async (orderId: string, songtekst: string): Promise<Order | null> => {
    try {
      // const response = await api.patch(`/api/orders/${orderId}`, { songtekst });
      // return response.data;
      
      // Mock update
      const order = mockOrders.find(o => o.order_id === orderId);
      if (order) {
        order.songtekst = songtekst;
      }
      return order || null;
    } catch (error) {
      console.error('Error updating songtext:', error);
      return null;
    }
  },

  // GET /api/orders/:id/download - download files
  downloadOrder: async (orderId: string, type: 'json' | 'txt'): Promise<string> => {
    try {
      // const response = await api.get(`/api/orders/${orderId}/download?type=${type}`);
      // return response.data;
      
      // Mock download data
      const order = mockOrders.find(o => o.order_id === orderId);
      if (!order) return '';
      
      if (type === 'json') {
        return JSON.stringify(order, null, 2);
      } else {
        return order.songtekst || 'Geen songtekst beschikbaar';
      }
    } catch (error) {
      console.error('Error downloading order:', error);
      return '';
    }
  }
};
