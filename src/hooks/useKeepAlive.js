import { useEffect } from "react";

const API_ROOT = "https://song-scribe-api-flow.onrender.com";

export default function useKeepAlive(intervalMs = 9 * 60 * 1000) {
  useEffect(() => {
    const ping = () => fetch(API_ROOT + "/").catch(() => {});
    ping();                              // ping direct bij mount
    const id = setInterval(ping, intervalMs);
    return () => clearInterval(id);      // opschonen bij unmount
  }, [intervalMs]);
}
