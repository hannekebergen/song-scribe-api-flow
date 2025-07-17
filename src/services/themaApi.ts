/**
 * API service voor Thema Management
 */

import { api } from './api';

// Types
export interface Thema {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  professional_prompt?: string;
  is_active: boolean;
  element_count?: number;
  created_at: string;
  updated_at: string;
  elements?: ThemaElement[];
  rhyme_sets?: ThemaRhymeSet[];
}

export interface ThemaElement {
  id: number;
  thema_id: number;
  element_type: string;
  content: string;
  usage_context?: string;
  weight: number;
  suno_format?: string;
  created_at: string;
}

export interface ThemaRhymeSet {
  id: number;
  thema_id: number;
  rhyme_pattern: string;
  rhyme_pairs: string[][];
  words?: string[]; // Backward compatibility
  difficulty_level: string;
  created_at: string;
}

export interface ThemaStats {
  total_themas: number;
  active_themas: number;
  inactive_themas: number;
  total_elements: number;
  recent_additions: number;
}

// Request types
export interface CreateThemaRequest {
  name: string;
  display_name: string;
  description?: string;
  professional_prompt?: string;
  is_active?: boolean;
}

export interface UpdateThemaRequest {
  name?: string;
  display_name?: string;
  description?: string;
  professional_prompt?: string;
  is_active?: boolean;
}

export interface CreateElementRequest {
  thema_id: number;
  element_type: string;
  content: string;
  usage_context?: string;
  weight?: number;
  suno_format?: string;
}

export interface UpdateElementRequest {
  element_type?: string;
  content?: string;
  usage_context?: string;
  weight?: number;
  suno_format?: string;
}

export interface CreateRhymeSetRequest {
  thema_id: number;
  rhyme_pattern: string;
  rhyme_pairs: string[][];
  difficulty_level?: string;
}

export interface UpdateRhymeSetRequest {
  rhyme_pattern?: string;
  rhyme_pairs?: string[][];
  difficulty_level?: string;
}

// API Service
export const themaApi = {
  // Statistics
  getStats: async (): Promise<ThemaStats> => {
    try {
      const response = await api.get<ThemaStats>('/api/admin/themes/stats');
      return response.data;
    } catch (error) {
      console.error('Error fetching thema stats:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch thema stats');
    }
  },

  // Themas
  getThemas: async (params?: {
    skip?: number;
    limit?: number;
    search?: string;
    active_only?: boolean;
  }): Promise<Thema[]> => {
    try {
      const response = await api.get<Thema[]>('/api/admin/themes', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching themas:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch themas');
    }
  },

  getThema: async (themaId: number): Promise<Thema> => {
    try {
      const response = await api.get<Thema>(`/api/admin/themes/${themaId}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching thema:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch thema');
    }
  },

  createThema: async (thema: CreateThemaRequest): Promise<Thema> => {
    try {
      const response = await api.post<Thema>('/api/admin/themes', thema);
      return response.data;
    } catch (error) {
      console.error('Error creating thema:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to create thema');
    }
  },

  updateThema: async (themaId: number, thema: UpdateThemaRequest): Promise<Thema> => {
    try {
      const response = await api.put<Thema>(`/api/admin/themes/${themaId}`, thema);
      return response.data;
    } catch (error) {
      console.error('Error updating thema:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to update thema');
    }
  },

  deleteThema: async (themaId: number): Promise<void> => {
    try {
      await api.delete(`/api/admin/themes/${themaId}`);
    } catch (error) {
      console.error('Error deleting thema:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to delete thema');
    }
  },

  // Elements
  getThemaElements: async (themaId: number, elementType?: string): Promise<ThemaElement[]> => {
    try {
      const params = elementType ? { element_type: elementType } : undefined;
      const response = await api.get<ThemaElement[]>(`/api/admin/themes/${themaId}/elements`, { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching thema elements:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch thema elements');
    }
  },

  createElement: async (element: CreateElementRequest): Promise<ThemaElement> => {
    try {
      const response = await api.post<ThemaElement>('/api/admin/elements', element);
      return response.data;
    } catch (error) {
      console.error('Error creating element:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to create element');
    }
  },

  updateElement: async (elementId: number, element: UpdateElementRequest): Promise<ThemaElement> => {
    try {
      const response = await api.put<ThemaElement>(`/api/admin/elements/${elementId}`, element);
      return response.data;
    } catch (error) {
      console.error('Error updating element:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to update element');
    }
  },

  deleteElement: async (elementId: number): Promise<void> => {
    try {
      await api.delete(`/api/admin/elements/${elementId}`);
    } catch (error) {
      console.error('Error deleting element:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to delete element');
    }
  },

  // Rhyme Sets
  getThemaRhymeSets: async (themaId: number): Promise<ThemaRhymeSet[]> => {
    try {
      const response = await api.get<ThemaRhymeSet[]>(`/api/admin/themes/${themaId}/rhyme-sets`);
      return response.data;
    } catch (error) {
      console.error('Error fetching rhyme sets:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch rhyme sets');
    }
  },

  createRhymeSet: async (rhymeSet: CreateRhymeSetRequest): Promise<ThemaRhymeSet> => {
    try {
      const response = await api.post<ThemaRhymeSet>('/api/admin/rhyme-sets', rhymeSet);
      return response.data;
    } catch (error) {
      console.error('Error creating rhyme set:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to create rhyme set');
    }
  },

  updateRhymeSet: async (rhymeSetId: number, rhymeSet: UpdateRhymeSetRequest): Promise<ThemaRhymeSet> => {
    try {
      const response = await api.put<ThemaRhymeSet>(`/api/admin/rhyme-sets/${rhymeSetId}`, rhymeSet);
      return response.data;
    } catch (error) {
      console.error('Error updating rhyme set:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to update rhyme set');
    }
  },

  deleteRhymeSet: async (rhymeSetId: number): Promise<void> => {
    try {
      await api.delete(`/api/admin/rhyme-sets/${rhymeSetId}`);
    } catch (error) {
      console.error('Error deleting rhyme set:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to delete rhyme set');
    }
  },

  // Bulk operations
  bulkToggleActive: async (themaIds: number[], isActive: boolean): Promise<{
    success_count: number;
    error_count: number;
    errors: string[];
  }> => {
    try {
      const response = await api.put<{
        success_count: number;
        error_count: number;
        errors: string[];
      }>('/api/admin/themes/bulk/toggle-active', {
        thema_ids: themaIds,
        is_active: isActive
      });
      return response.data;
    } catch (error) {
      console.error('Error bulk toggling themas:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to bulk toggle themas');
    }
  }
}; 