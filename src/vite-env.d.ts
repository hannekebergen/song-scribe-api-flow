/// <reference types="vite/client" />

/**
 * Custom environment variables for the Song-Scribe API project
 */
interface ImportMetaEnv {
  readonly VITE_API_URL: string;
  readonly VITE_API_KEY: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
