import { useEffect } from "react";

const API_ROOT = import.meta.env.VITE_API_URL;

export default function useKeepAlive(intervalMs = 5 * 60 * 1000) {
  useEffect(() => {
    // Gebruik HEAD request in plaats van GET om payload te minimaliseren
    const ping = () => fetch(API_ROOT + "/", { 
      method: "HEAD",
      mode: "no-cors" 
    }).catch(() => {});
    
    // Ping direct bij mount
    ping();
    
    // Periodieke ping elke 5 minuten (of zoals geconfigureerd)
    const id = setInterval(ping, intervalMs);
    
    // Opschonen bij unmount
    return () => clearInterval(id);
  }, [intervalMs]);
}
