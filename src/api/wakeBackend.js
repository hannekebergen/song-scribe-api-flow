const API = "https://song-scribe-api-flow.onrender.com";

export async function wakeBackend() {
  // Cold ping zonder CORS
  await fetch(API + "/", { mode: "no-cors" }).catch(() => {});
  const start = Date.now();
  while (Date.now() - start < 10000) {          // max 10 s
    try {
      const r = await fetch(API + "/", { method: "HEAD" });
      if (r.ok) return;
    } catch { /* ignore */ }
    await new Promise(r => setTimeout(r, 500)); // 0,5 s
  }
}
