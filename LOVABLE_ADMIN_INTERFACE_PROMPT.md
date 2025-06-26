# 🎵 Song Scribe Thema Database - Dashboard Integration

## 📋 Project Overview
Add a **Thema Management** section to the existing Song Scribe dashboard. This will be integrated as tabs/sections within the current dashboard, maintaining the same design system and user experience.

## 🎯 Integration Requirements

### **Current Dashboard Structure:**
- **Dashboard.tsx**: Main dashboard with orders overview
- **Navigation**: React Router with `/dashboard`, `/orders/:id`, etc.
- **Design System**: Tailwind CSS with blue/indigo gradient theme
- **Components**: Already uses shadcn/ui components

### **Integration Approach:**
Add a **tabbed interface** to the existing dashboard with:
1. **Orders Tab** (existing functionality)
2. **Thema Management Tab** (new - what we're building)
3. **Analytics Tab** (future expansion)

## 🔧 Technical Integration

### **1. Update Dashboard.tsx with Tabs**
Add a tab system using shadcn/ui tabs component:

```tsx
// Add to existing Dashboard.tsx
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

// In Dashboard component:
<Tabs defaultValue="orders" className="space-y-8">
  <TabsList className="grid w-full grid-cols-3">
    <TabsTrigger value="orders">📦 Orders</TabsTrigger>
    <TabsTrigger value="thema">🎵 Thema's</TabsTrigger>
    <TabsTrigger value="analytics">📊 Analytics</TabsTrigger>
  </TabsList>
  
  <TabsContent value="orders">
    {/* Existing orders content */}
  </TabsContent>
  
  <TabsContent value="thema">
    <ThemaManagement />
  </TabsContent>
  
  <TabsContent value="analytics">
    <div>Analytics coming soon...</div>
  </TabsContent>
</Tabs>
```

### **2. Create ThemaManagement Component**
New component: `src/components/dashboard/ThemaManagement.tsx`

```tsx
// Component structure to build
interface ThemaManagementProps {}

const ThemaManagement = () => {
  return (
    <div className="space-y-6">
      {/* Stats cards for themes */}
      <ThemaStatsCards />
      
      {/* Quick actions */}
      <ThemaQuickActions />
      
      {/* Thema list with management */}
      <ThemaList />
    </div>
  );
};
```

## 🎨 Design Integration

### **Match Existing Design System:**
- **Color Scheme**: Same blue/indigo gradients as current dashboard
- **Typography**: Consistent with existing headers and text
- **Card Style**: Same card styling as StatsCards and FetchOrdersCard
- **Spacing**: Consistent `space-y-8`, `space-y-6` patterns
- **Responsive**: Same `container mx-auto px-6 py-8` structure

### **Component Structure:**

#### **ThemaStatsCards**
```tsx
// Mirror existing StatsCards.tsx pattern
const ThemaStatsCards = () => (
  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
    <Card className="bg-gradient-to-br from-blue-50 to-blue-100 border-blue-200">
      <CardContent className="p-6">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-blue-600 text-sm font-medium">Totaal Thema's</p>
            <p className="text-2xl font-bold text-blue-800">{totalThemas}</p>
          </div>
          <div className="h-12 w-12 bg-blue-500 rounded-lg flex items-center justify-center">
            <ThemeIcon className="h-6 w-6 text-white" />
          </div>
        </div>
      </CardContent>
    </Card>
    {/* More stat cards */}
  </div>
);
```

#### **ThemaQuickActions**
```tsx
// Similar to FetchOrdersCard styling
const ThemaQuickActions = () => (
  <Card className="bg-gradient-to-br from-green-50 to-emerald-100 border-green-200">
    <CardContent className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-green-800">Thema Beheer</h3>
      </div>
      <div className="space-y-3">
        <Button className="w-full bg-green-600 hover:bg-green-700">
          <PlusIcon className="h-4 w-4 mr-2" />
          Nieuw Thema
        </Button>
        <Button variant="outline" className="w-full">
          <UploadIcon className="h-4 w-4 mr-2" />
          Import CSV
        </Button>
      </div>
    </CardContent>
  </Card>
);
```

## 🔗 API Integration

### **Extend Existing API Structure**
Add thema endpoints to current API service:

```typescript
// Extend src/services/api.ts
export const themaApi = {
  // GET /api/admin/themes
  getThemas: async (): Promise<Thema[]> => {
    const response = await api.get<Thema[]>('/api/admin/themes');
    return response.data;
  },
  
  // POST /api/admin/themes
  createThema: async (thema: CreateThemaRequest): Promise<Thema> => {
    const response = await api.post<Thema>('/api/admin/themes', thema);
    return response.data;
  },
  
  // PUT /api/admin/themes/:id
  updateThema: async (id: number, thema: UpdateThemaRequest): Promise<Thema> => {
    const response = await api.put<Thema>(`/api/admin/themes/${id}`, thema);
    return response.data;
  },
  
  // DELETE /api/admin/themes/:id
  deleteThema: async (id: number): Promise<void> => {
    await api.delete(`/api/admin/themes/${id}`);
  },
};
```

### **Custom Hooks**
Create hooks similar to existing `useFetchOrders`:

```typescript
// src/hooks/useThemas.ts
export const useThemas = () => {
  const [themas, setThemas] = useState<Thema[]>([]);
  const [loading, setLoading] = useState(false);
  
  const fetchThemas = async () => {
    setLoading(true);
    try {
      const data = await themaApi.getThemas();
      setThemas(data);
    } catch (error) {
      console.error('Failed to fetch themas:', error);
    } finally {
      setLoading(false);
    }
  };
  
  return { themas, loading, fetchThemas };
};
```

## 📱 User Experience

### **Navigation Flow:**
1. **User lands on Dashboard** → Sees Orders tab active
2. **Clicks "🎵 Thema's" tab** → Switches to thema management
3. **All functionality within tabs** → No page navigation needed
4. **Consistent header/layout** → Same JouwSong branding

### **Responsive Design:**
- **Desktop**: Full tabbed interface with side-by-side layouts
- **Tablet**: Stacked cards, collapsible sections
- **Mobile**: Single column, touch-friendly controls

## 🚀 Implementation Priority

### **Phase 1 (MVP Integration):**
1. Add Tabs component to Dashboard.tsx
2. Create basic ThemaManagement component
3. Add ThemaStatsCards (read-only)
4. Basic ThemaList with view/edit capabilities

### **Phase 2 (Full CRUD):**
1. Add/Edit/Delete thema functionality
2. Element management (keywords, power phrases, etc.)
3. Bulk operations
4. CSV import/export

### **Phase 3 (Advanced Features):**
1. Rhyme set management
2. Usage analytics within thema tab
3. Integration with AI prompt preview
4. Theme templates and suggestions

## 🎵 Nederlandse Context Integration

### **Maintain Existing Patterns:**
- **Language**: Keep Dutch labels consistent with existing dashboard
- **Terminology**: Use same terms as orders section ("Beheer", "Overzicht", etc.)
- **Icons**: Use consistent icon style from existing dashboard
- **Success/Error messages**: Same toast notification style

### **Example Labels:**
- "Thema Beheer" (instead of "Theme Management")
- "Nieuwe Thema" (instead of "New Theme")  
- "Elementen per Thema" (instead of "Elements per Theme")
- "Rijmwoorden" (instead of "Rhyme Words")

---

## 📋 Implementation Checklist

**Build this as integrated tabs within the existing JouwSong dashboard:**

- [ ] Add shadcn/ui Tabs to existing Dashboard.tsx
- [ ] Create ThemaManagement component matching existing style
- [ ] Extend API service with thema endpoints
- [ ] Create useThemas hook similar to useFetchOrders
- [ ] Implement ThemaStatsCards matching StatsCards pattern
- [ ] Add ThemaQuickActions matching FetchOrdersCard style
- [ ] Ensure responsive design matches existing dashboard
- [ ] Maintain Dutch language consistency

**This approach provides seamless integration while reusing the existing design system and navigation patterns.** 