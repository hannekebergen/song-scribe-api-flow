/**
 * API configuration with fallback URL
 */

// Use environment variable with fallback to Render URL
const API = import.meta.env.VITE_API_URL ?? 'https://song-scribe-api-flow.onrender.com';

// Log warning if environment variable is missing
if (!import.meta.env.VITE_API_URL) {
  console.warn('VITE_API_URL is undefined; using fallback:', API);
}

export { API };
