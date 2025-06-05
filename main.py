from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import logging
import os

# Importeer routers
from app.routers.songs import router as songs_router
from app.routers.orders import router as orders_router

# Importeer database en services
from app.db.session import get_db, init_db
from app.services.plugpay_client import fetch_and_store_recent_orders, PlugPayAPIError
from app.auth.token import get_api_key

app = FastAPI(
    title="JouwSong.nl API",
    description="Backend API voor jouwsong.nl om songtekstprompts te genereren",
    version="0.1.0"
)

# CORS configuratie voor frontend toegang vanaf Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://song-scribe-api-flow.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialiseer de database bij het opstarten van de app
@app.on_event("startup")
def startup_db_client():
    try:
        init_db()
        logging.info("Database succesvol geïnitialiseerd")
    except Exception as e:
        logging.error(f"Fout bij initialiseren van database: {str(e)}")

# Voeg routers toe
app.include_router(songs_router, prefix="/api/songs", tags=["songs"])
app.include_router(orders_router, prefix="/orders", tags=["orders"])

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

@app.get("/")
async def root():
    return {"message": "Welkom bij de JouwSong.nl API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
