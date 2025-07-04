/**
 * AI API Service voor songtekst generatie en prompt verbetering
 */

import { api } from './api';

// Types voor AI API requests en responses
export interface GenerateSongtextRequest {
  prompt: string;
  provider?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface GenerateFromOrderRequest {
  order_id: number;
  provider?: string;
  temperature?: number;
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
   * Genereer een songtekst op basis van een prompt
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
  }
};

// Convenience functions voor veelgebruikte operaties
export const generateSongtextFromOrder = async (
  orderId: number, 
  provider?: string, 
  temperature?: number
): Promise<SongtextResponse> => {
  return aiApi.generateFromOrder({
    order_id: orderId,
    provider,
    temperature
  });
};

export const generateSongtextFromPrompt = async (
  prompt: string,
  provider?: string,
  options?: { max_tokens?: number; temperature?: number }
): Promise<SongtextResponse> => {
  return aiApi.generateSongtext({
    prompt,
    provider,
    max_tokens: options?.max_tokens,
    temperature: options?.temperature
  });
};

export default aiApi; 