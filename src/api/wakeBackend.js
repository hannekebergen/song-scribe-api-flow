const API = "https://song-scribe-api-flow.onrender.com";

export async function wakeBackend() {
  await fetch(API + "/", { mode: "no-cors" }).catch(() => {});
  await new Promise(r => setTimeout(r, 8000));  // 8 s wachten
}
