/**
 * React hooks voor Thema Management
 */

import { useState, useEffect, useCallback } from 'react';
import { themaApi, Thema, ThemaStats, ThemaElement, ThemaRhymeSet } from '../services/themaApi';
import { useToast } from '../hooks/use-toast';

// Hook voor thema statistics
export const useThemaStats = () => {
  const [stats, setStats] = useState<ThemaStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const fetchStats = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await themaApi.getStats();
      setStats(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch stats';
      setError(errorMessage);
      toast({
        title: "Fout bij laden statistieken",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  }, [toast]);

  useEffect(() => {
    fetchStats();
  }, [fetchStats]);

  return { stats, loading, error, refetch: fetchStats };
};

// Hook voor thema lijst
export const useThemas = (initialParams?: {
  skip?: number;
  limit?: number;
  search?: string;
  active_only?: boolean;
}) => {
  const [themas, setThemas] = useState<Thema[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [params, setParams] = useState(initialParams || {});
  const { toast } = useToast();

  const fetchThemas = useCallback(async (newParams?: typeof params) => {
    try {
      setLoading(true);
      setError(null);
      const searchParams = newParams || params;
      const data = await themaApi.getThemas(searchParams);
      setThemas(data);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch themas';
      setError(errorMessage);
      toast({
        title: "Fout bij laden thema's",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  }, [params, toast]);

  useEffect(() => {
    fetchThemas();
  }, [fetchThemas]);

  const updateParams = useCallback((newParams: Partial<typeof params>) => {
    const updatedParams = { ...params, ...newParams };
    setParams(updatedParams);
    fetchThemas(updatedParams);
  }, [params, fetchThemas]);

  return { 
    themas, 
    loading, 
    error, 
    refetch: fetchThemas,
    updateParams,
    params
  };
};

// Hook voor CRUD operaties
export const useThemaCRUD = () => {
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const createThema = useCallback(async (themaData: {
    name: string;
    display_name: string;
    description?: string;
    is_active?: boolean;
  }) => {
    try {
      setLoading(true);
      const newThema = await themaApi.createThema(themaData);
      toast({
        title: "Thema aangemaakt",
        description: `Thema '${newThema.display_name}' is succesvol aangemaakt`,
      });
      return newThema;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create thema';
      toast({
        title: "Fout bij aanmaken thema",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const updateThema = useCallback(async (themaId: number, themaData: {
    name?: string;
    display_name?: string;
    description?: string;
    is_active?: boolean;
  }) => {
    try {
      setLoading(true);
      const updatedThema = await themaApi.updateThema(themaId, themaData);
      toast({
        title: "Thema bijgewerkt",
        description: `Thema '${updatedThema.display_name}' is succesvol bijgewerkt`,
      });
      return updatedThema;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update thema';
      toast({
        title: "Fout bij bijwerken thema",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const deleteThema = useCallback(async (themaId: number, themaName: string) => {
    try {
      setLoading(true);
      await themaApi.deleteThema(themaId);
      toast({
        title: "Thema verwijderd",
        description: `Thema '${themaName}' is succesvol verwijderd`,
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete thema';
      toast({
        title: "Fout bij verwijderen thema",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const bulkToggleActive = useCallback(async (themaIds: number[], isActive: boolean) => {
    try {
      setLoading(true);
      const result = await themaApi.bulkToggleActive(themaIds, isActive);
      toast({
        title: "Bulk actie voltooid",
        description: `${result.success_count} thema's ${isActive ? 'geactiveerd' : 'gedeactiveerd'}`,
      });
      return result;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to bulk toggle themas';
      toast({
        title: "Fout bij bulk actie",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  return {
    createThema,
    updateThema,
    deleteThema,
    bulkToggleActive,
    loading
  };
};

// Hook voor thema details (met elementen en rijmsets)
export const useThemaDetails = (themaId: number | null) => {
  const [thema, setThema] = useState<Thema | null>(null);
  const [elements, setElements] = useState<ThemaElement[]>([]);
  const [rhymeSets, setRhymeSets] = useState<ThemaRhymeSet[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const fetchThemaDetails = useCallback(async () => {
    if (!themaId) return;
    
    try {
      setLoading(true);
      setError(null);
      
      const [themaData, elementsData, rhymeSetsData] = await Promise.all([
        themaApi.getThema(themaId),
        themaApi.getThemaElements(themaId),
        themaApi.getThemaRhymeSets(themaId)
      ]);
      
      setThema(themaData);
      setElements(elementsData);
      setRhymeSets(rhymeSetsData);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to fetch thema details';
      setError(errorMessage);
      toast({
        title: "Fout bij laden thema details",
        description: errorMessage,
        variant: "destructive"
      });
    } finally {
      setLoading(false);
    }
  }, [themaId, toast]);

  useEffect(() => {
    fetchThemaDetails();
  }, [fetchThemaDetails]);

  return {
    thema,
    elements,
    rhymeSets,
    loading,
    error,
    refetch: fetchThemaDetails
  };
};

// Hook voor element CRUD
export const useElementCRUD = () => {
  const [loading, setLoading] = useState(false);
  const { toast } = useToast();

  const createElement = useCallback(async (elementData: {
    thema_id: number;
    element_type: string;
    content: string;
    usage_context?: string;
    weight?: number;
    suno_format?: string;
  }) => {
    try {
      setLoading(true);
      const newElement = await themaApi.createElement(elementData);
      toast({
        title: "Element aangemaakt",
        description: `Element '${newElement.content}' is succesvol aangemaakt`,
      });
      return newElement;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to create element';
      toast({
        title: "Fout bij aanmaken element",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const updateElement = useCallback(async (elementId: number, elementData: {
    element_type?: string;
    content?: string;
    usage_context?: string;
    weight?: number;
    suno_format?: string;
  }) => {
    try {
      setLoading(true);
      const updatedElement = await themaApi.updateElement(elementId, elementData);
      toast({
        title: "Element bijgewerkt",
        description: `Element '${updatedElement.content}' is succesvol bijgewerkt`,
      });
      return updatedElement;
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to update element';
      toast({
        title: "Fout bij bijwerken element",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  const deleteElement = useCallback(async (elementId: number, elementContent: string) => {
    try {
      setLoading(true);
      await themaApi.deleteElement(elementId);
      toast({
        title: "Element verwijderd",
        description: `Element '${elementContent}' is succesvol verwijderd`,
      });
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to delete element';
      toast({
        title: "Fout bij verwijderen element",
        description: errorMessage,
        variant: "destructive"
      });
      throw err;
    } finally {
      setLoading(false);
    }
  }, [toast]);

  return {
    createElement,
    updateElement,
    deleteElement,
    loading
  };
}; 