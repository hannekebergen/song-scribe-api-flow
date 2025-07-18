import { useEffect } from "react";
import { API } from "../api/config";

export default function useKeepAlive(intervalMs = 5 * 60 * 1000) {
  useEffect(() => {
    // Gebruik HEAD request in plaats van GET om payload te minimaliseren
    const ping = () => fetch(API + "/", { 
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
