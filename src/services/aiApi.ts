/**
 * AI API Service voor songtekst generatie en prompt verbetering
 */

import { api } from './api';

// Types voor AI API requests en responses
export interface GenerateSongtextRequest {
  beschrijving: string;
  provider?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface ProfessionalSongtextRequest {
  beschrijving: string;
  max_tokens?: number;
  temperature?: number;
}

export interface GenerateFromOrderRequest {
  order_id: number;
  provider?: string;
  max_tokens?: number;
  temperature?: number;
  use_suno?: boolean;
  use_professional_prompt?: boolean;
  auto_professional?: boolean;
}

export interface EnhancePromptRequest {
  original_prompt: string;
  order_id: number;
  provider?: string;
}

export interface ExtendSongtextRequest {
  original_songtext: string;
  extension_type: string;
  additional_info?: string;
  provider?: string;
}

// Suno API types
export interface GenerateMusicRequest {
  // Custom Mode parameters
  customMode: boolean;
  instrumental: boolean;
  model: string;
  
  // Required in Custom Mode
  style?: string;
  title?: string;
  
  // Prompt - required if instrumental is false in Custom Mode
  prompt?: string;
  
  // Optional parameters
  negativeTags?: string;
  
  // Legacy support for old API calls
  songtext?: string;
}

export interface GenerateMusicFromOrderRequest {
  order_id: number;
  style?: string;
  instrumental?: boolean;
  title?: string;
}

export interface MusicResponse {
  success: boolean;
  song_id?: string;
  title?: string;
  audio_url?: string;
  video_url?: string;
  image_url?: string;
  style?: string;
  model?: string;
  created_at?: string;
  generated_at?: string;
  error?: string;
}

export interface SunoHealthResponse {
  status: string;
  has_suno_key: boolean;
  base_url: string;
}

export interface AIResponse {
  success: boolean;
  provider: string;
  tokens_used?: number;
  generated_at: string;
}

export interface SongtextResponse extends AIResponse {
  songtext: string;
  prompt_length: number;
  is_dummy?: boolean;
}

export interface PromptEnhancementResponse extends AIResponse {
  enhanced_prompt: string;
  original_prompt: string;
}

export interface ExtensionResponse extends AIResponse {
  extended_songtext: string;
  original_songtext: string;
  extension_type: string;
}

export interface AIProvider {
  name: string;
  available: boolean;
  display_name: string;
}

export interface ProvidersResponse {
  providers: AIProvider[];
  default_provider: string;
}

export interface HealthResponse {
  status: string;
  default_provider: string;
  has_openai_key: boolean;
  has_claude_key: boolean;
  has_gemini_key: boolean;
}

/**
 * AI API service voor alle AI-gerelateerde operaties
 */
export const aiApi = {
  /**
   * Genereer een songtekst op basis van een beschrijving
   */
  generateSongtext: async (request: GenerateSongtextRequest): Promise<SongtextResponse> => {
    try {
      const response = await api.post<SongtextResponse>('/api/ai/generate-songtext', request);
      return response.data;
    } catch (error) {
      console.error('Error generating songtext:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate songtext');
    }
  },

  /**
   * Genereer een professionele songtekst met uitgebreide prompt
   */
  generateProfessionalSongtext: async (request: ProfessionalSongtextRequest): Promise<SongtextResponse> => {
    try {
      const response = await api.post<SongtextResponse>('/api/ai/generate-professional-songtext', request);
      return response.data;
    } catch (error) {
      console.error('Error generating professional songtext:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate professional songtext');
    }
  },

  /**
   * Genereer een songtekst direct van een order
   */
  generateFromOrder: async (request: GenerateFromOrderRequest): Promise<SongtextResponse> => {
    try {
      const response = await api.post<SongtextResponse>('/api/ai/generate-from-order', request);
      return response.data;
    } catch (error) {
      console.error('Error generating songtext from order:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate songtext from order');
    }
  },

  /**
   * Verbeter een bestaande prompt
   */
  enhancePrompt: async (request: EnhancePromptRequest): Promise<PromptEnhancementResponse> => {
    try {
      const response = await api.post<PromptEnhancementResponse>('/api/ai/enhance-prompt', request);
      return response.data;
    } catch (error) {
      console.error('Error enhancing prompt:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to enhance prompt');
    }
  },

  /**
   * Breid een songtekst uit (voor upsells)
   */
  extendSongtext: async (request: ExtendSongtextRequest): Promise<ExtensionResponse> => {
    try {
      const response = await api.post<ExtensionResponse>('/api/ai/extend-songtext', request);
      return response.data;
    } catch (error) {
      console.error('Error extending songtext:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to extend songtext');
    }
  },

  /**
   * Haal beschikbare AI providers op
   */
  getProviders: async (): Promise<ProvidersResponse> => {
    try {
      const response = await api.get<ProvidersResponse>('/api/ai/providers');
      return response.data;
    } catch (error) {
      console.error('Error fetching AI providers:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to fetch AI providers');
    }
  },

  /**
   * Check AI service health
   */
  healthCheck: async (): Promise<HealthResponse> => {
    try {
      const response = await api.get<HealthResponse>('/api/ai/health');
      return response.data;
    } catch (error) {
      console.error('Error checking AI health:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to check AI health');
    }
  },

  /**
   * Genereer volledige muziek via Suno API
   */
  generateMusic: async (request: GenerateMusicRequest): Promise<MusicResponse> => {
    try {
      const response = await api.post<MusicResponse>('/api/ai/generate-music', request);
      return response.data;
    } catch (error) {
      console.error('Error generating music:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate music');
    }
  },

  /**
   * Genereer muziek op basis van een order
   */
  generateMusicFromOrder: async (request: GenerateMusicFromOrderRequest): Promise<MusicResponse> => {
    try {
      const response = await api.post<MusicResponse>('/api/ai/generate-music-from-order', request);
      return response.data;
    } catch (error) {
      console.error('Error generating music from order:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to generate music from order');
    }
  },

  /**
   * Controleer status van een Suno song
   */
  getSunoSongStatus: async (songId: string): Promise<any> => {
    try {
      const response = await api.get(`/api/ai/suno-status/${songId}`);
      return response.data;
    } catch (error) {
      console.error('Error checking Suno song status:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to check song status');
    }
  },

  /**
   * Check Suno API health
   */
  sunoHealthCheck: async (): Promise<SunoHealthResponse> => {
    try {
      const response = await api.get<SunoHealthResponse>('/api/ai/suno-health');
      return response.data;
    } catch (error) {
      console.error('Error checking Suno health:', error);
      throw new Error(error instanceof Error ? error.message : 'Failed to check Suno health');
    }
  }
};

// Convenience functions voor veelgebruikte operaties
export const generateSongtextFromOrder = async (
  orderId: number, 
  provider?: string, 
  temperature?: number,
  useProfessional?: boolean
): Promise<SongtextResponse> => {
  return aiApi.generateFromOrder({
    order_id: orderId,
    provider,
    temperature,
    use_professional_prompt: useProfessional,
    auto_professional: true
  });
};

export const generateSongtextFromDescription = async (
  beschrijving: string,
  provider?: string,
  options?: { max_tokens?: number; temperature?: number }
): Promise<SongtextResponse> => {
  return aiApi.generateSongtext({
    beschrijving,
    provider,
    max_tokens: options?.max_tokens,
    temperature: options?.temperature
  });
};

export const generateProfessionalSongtextFromDescription = async (
  beschrijving: string,
  options?: { max_tokens?: number; temperature?: number }
): Promise<SongtextResponse> => {
  return aiApi.generateProfessionalSongtext({
    beschrijving,
    max_tokens: options?.max_tokens,
    temperature: options?.temperature
  });
};

export default aiApi; 