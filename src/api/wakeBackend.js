const API = "https://song-scribe-api-flow.onrender.com";

export async function wakeBackend() {
  // Cold ping zonder CORS
  await fetch(API + "/", { mode: "no-cors" }).catch(() => {});
  await new Promise(r => setTimeout(r, 2500));
}
