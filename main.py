from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, BackgroundTasks, Response
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import logging
import os
import time
import asyncio
from starlette.middleware.base import BaseHTTPMiddleware

# Configure logging level from environment variables
logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO").upper())

# Importeer routers
from app.routers.songs import router as songs_router
from app.routers.orders import router as orders_router
from app.routers.ai import router as ai_router
from app.routers.admin import router as admin_router

# Importeer database en services
from app.db.session import get_db, init_db
from app.services.plugpay_client import fetch_and_store_recent_orders, PlugPayAPIError
from app.auth.token import get_api_key

app = FastAPI(
    title="JouwSong.nl API",
    description="Backend API voor jouwsong.nl om songtekstprompts te genereren",
    version="0.1.0"
)

# Simple request logger middleware
class SimpleLogger(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.time()
        response = await call_next(request)
        duration = (time.time() - start) * 1000
        origin = request.headers.get("origin")
        print(
            f"{request.method} {request.url.path} "
            f"status={response.status_code} "
            f"origin={origin or '-'} took={duration:.0f}ms"
        )
        return response

app.add_middleware(SimpleLogger)

# CORS configuratie voor frontend toegang vanaf Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://song-scribe-api-flow.vercel.app"],  # specifiek alleen de Vercel frontend
    allow_credentials=True,  # cookies toestaan voor auth
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint voor Render
@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

# Initialiseer de database bij het opstarten van de app
@app.on_event("startup")
async def startup_db_client():
    try:
        # Korte vertraging om ervoor te zorgen dat de server volledig is opgestart
        # voordat we health checks accepteren
        await asyncio.sleep(2)  # 2 seconden wachten
        
        init_db()
        logging.info("Database succesvol geïnitialiseerd")
    except Exception as e:
        logging.error(f"Fout bij initialiseren van database: {str(e)}")

# Voeg routers toe
app.include_router(songs_router, prefix="/api/songs", tags=["songs"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])
app.include_router(ai_router, tags=["ai"])
app.include_router(admin_router, tags=["admin"])

# Admin route voor het handmatig ophalen van bestellingen
@app.post("/api/admin/fetch-orders", tags=["admin"])
async def admin_fetch_orders(
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """
    Haalt recente bestellingen op van Plug&Pay en slaat ze op in de database.
    Deze taak wordt op de achtergrond uitgevoerd.
    
    Vereist API-key authenticatie.
    """
    try:
        # Voer de taak uit op de achtergrond
        background_tasks.add_task(fetch_and_store_recent_orders, db)
        return {"status": "Bestellingen worden op de achtergrond opgehaald en verwerkt"}
    except PlugPayAPIError as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welkom bij de JouwSong.nl API"}

@app.head("/", include_in_schema=False)
async def root_head():
    # Render verwacht alleen status 200, geen body
    return Response(status_code=200)

if __name__ == "__main__":
    import uvicorn
    # Use PORT environment variable with fallback to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
