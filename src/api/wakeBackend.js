const API = "https://song-scribe-api-flow.onrender.com";

export async function wakeBackend() {
  // Initial ping to wake up the backend
  await fetch(API + "/", { mode: "no-cors" }).catch(() => {});
  
  // Poll with HEAD requests until backend is responsive or timeout
  const startTime = Date.now();
  const timeout = 30000; // 30 seconds timeout
  const interval = 1000; // 1 second interval
  
  while (Date.now() - startTime < timeout) {
    try {
      // Use HEAD request with no-cors mode to check if backend is awake
      await fetch(API + "/", { 
        method: "HEAD",
        mode: "no-cors"
      });
      
      // If we get here without error, backend might be ready
      return;
    } catch (error) {
      // Wait for the next interval
      await new Promise(r => setTimeout(r, interval));
    }
  }
  
  // If we get here, we've exceeded the timeout
  throw new Error("Backend wake-up timed out after 30 seconds");
}
