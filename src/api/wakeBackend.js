const API = "https://song-scribe-api-flow.onrender.com";

/**
 * Eenvoudige functie om de backend te wekken met een enkele HEAD request.
 * Gebruikt no-cors mode om CORS-issues te vermijden.
 * 
 * Deze functie is vereenvoudigd om dubbele pings te voorkomen, aangezien
 * useKeepAlive.js al periodieke pings verzorgt.
 */
export async function wakeBackend() {
  // Enkele HEAD request om de backend te wekken
  return fetch(API + "/", { 
    method: "HEAD",
    mode: "no-cors"
  }).catch(() => {
    // Stil falen - geen error throwing
    // De useKeepAlive hook zal periodiek blijven pingen
  });
}
