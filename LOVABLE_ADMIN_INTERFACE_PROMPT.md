# 🎵 Song Scribe Thema Database Admin Interface

## 📋 Project Overview
Build a modern, professional admin interface for managing a **Song Theme Database** that powers AI songtext generation. The system manages themes (like "verjaardag", "liefde", "huwelijk") with their associated elements (keywords, power phrases, musical parameters, rhyme sets).

## 🎯 Core Requirements

### **1. Dashboard Overview**
- **Stats Cards**: Total themes, active themes, total elements, recent additions
- **Quick Actions**: Add new theme, bulk import, database backup
- **Recent Activity**: Last modified themes and elements
- **Usage Analytics**: Most used themes, element popularity charts

### **2. Theme Management**
**Theme List View:**
- Searchable/filterable table with themes
- Show: Name, Display Name, Element Count, Status (Active/Inactive), Last Modified
- Bulk actions: Activate/Deactivate, Delete, Export
- Quick edit toggle for active/inactive status

**Theme Detail/Edit:**
- Basic Info: Name (slug), Display Name, Description
- Status toggle (Active/Inactive)
- Element counts by type (visual stats)
- Tabs for different element types

### **3. Element Management System**

**Element Types to Support:**
- **Keywords** (thema-gerelateerde woorden)
- **Power Phrases** (krachtige zinnen voor refrein/chorus)
- **Genres** (pop, rock, ballad, etc.)
- **BPM** (tempo suggestions)
- **Key** (toonsoort: C majeur, A mineur, etc.)
- **Instruments** (piano, guitar, drums, etc.)
- **Effects** (warm tone, reverb, etc.)
- **Verse Starters** (openingszinnen)

**Element Form Fields:**
- Element Type (dropdown)
- Content (textarea for longer texts)
- Usage Context (dropdown: intro/verse/chorus/bridge/any)
- Weight (1-10 for random selection priority)
- Suno Format (optional Suno.ai specific formatting)

### **4. Rhyme Set Management**
- **Rhyme Pattern** (AABB, ABAB, ABCB, etc.)
- **Word List** (dynamic array input)
- **Difficulty Level** (easy/medium/hard)
- Rhyme validation (check if words actually rhyme)

### **5. Bulk Operations**
- **CSV Import/Export** for themes and elements
- **Duplicate Theme** with all elements
- **Template Creation** from existing themes
- **Bulk Edit** elements across themes

## 🎨 UI/UX Requirements

### **Design System:**
- **Framework**: Use Tailwind CSS + Headless UI or shadcn/ui
- **Colors**: Professional blue/gray theme with green accents for active states
- **Typography**: Clean, readable fonts (Inter or similar)
- **Icons**: Heroicons or Lucide icons

### **Layout:**
- **Sidebar Navigation**: Dashboard, Themes, Elements, Rhyme Sets, Settings
- **Top Bar**: Search, User menu, Quick actions
- **Responsive**: Mobile-first design
- **Dark Mode**: Toggle support

### **Components Needed:**
- Data tables with sorting/filtering
- Multi-select dropdowns
- Tag inputs for arrays
- Rich text editor for descriptions
- Confirmation modals for destructive actions
- Toast notifications for feedback
- Drag-and-drop for reordering

## 🔧 Technical Specifications

### **API Integration:**
```typescript
// Base API endpoints to implement
const API_BASE = '/api/admin/themes'

interface Theme {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  elements: ThemeElement[];
  rhyme_sets: RhymeSet[];
}

interface ThemeElement {
  id: number;
  thema_id: number;
  element_type: string;
  content: string;
  usage_context?: string;
  weight: number;
  suno_format?: string;
  created_at: string;
}

interface RhymeSet {
  id: number;
  thema_id: number;
  rhyme_pattern: string;
  words: string[];
  difficulty_level: string;
  created_at: string;
}
```

### **Key Features:**
- **Search & Filter**: Real-time search across themes and elements
- **Validation**: Form validation with clear error messages
- **Auto-save**: Draft saving for long forms
- **History/Audit**: Track changes with timestamps
- **Permissions**: Admin-only access with API key authentication

## 🚀 Implementation Priority

### **Phase 1 (MVP):**
1. Theme CRUD (Create, Read, Update, Delete)
2. Element management per theme
3. Basic dashboard with stats
4. Search and filtering

### **Phase 2 (Enhanced):**
1. Rhyme set management
2. Bulk import/export
3. Advanced filtering and sorting
4. Usage analytics

### **Phase 3 (Advanced):**
1. Theme templates
2. AI-powered rhyme suggestions
3. Element usage statistics
4. Integration with main Song Scribe app

## 💡 Special Features

### **Smart Suggestions:**
- **Rhyme Assistant**: When adding rhyme sets, suggest rhyming words
- **Element Templates**: Pre-fill common elements for theme types
- **Duplicate Detection**: Warn about similar elements within theme

### **Testing Integration:**
- **Preview Generator**: Test theme data with live prompt generation
- **Element Effectiveness**: Track which elements are most used
- **A/B Testing**: Compare different element variations

## 🔗 Integration Points

### **Main Song Scribe App:**
- API endpoints to consume theme data
- Real-time updates when themes are modified
- Usage tracking from main app back to admin

### **Export Formats:**
- **CSV**: For spreadsheet editing
- **JSON**: For backup/migration
- **SQL**: For direct database import

## 📱 User Experience Flow

1. **Login** → Admin dashboard
2. **Dashboard** → Quick overview + navigation
3. **Theme List** → Browse/search themes
4. **Theme Detail** → Edit theme + manage elements
5. **Element Management** → Add/edit/delete elements
6. **Bulk Operations** → Import/export/duplicate

## 🎵 Nederlandse Context
- **Interface Language**: Dutch labels and descriptions
- **Content Examples**: Use Dutch song themes and terminology
- **Validation**: Dutch language validation for content fields
- **Help Text**: Contextual help in Dutch

---

**Build this as a single-page application with modern React/TypeScript, focusing on usability and efficiency for content managers who will be adding hundreds of theme elements.** 