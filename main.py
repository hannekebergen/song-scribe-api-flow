from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import songs

app = FastAPI(
    title="JouwSong.nl API",
    description="Backend API voor jouwsong.nl om songtekstprompts te genereren",
    version="0.1.0"
)

# CORS configuratie voor frontend toegang (bijv. vanaf Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In productie: vervang door specifieke origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers toevoegen
app.include_router(songs.router)

@app.get("/")
async def root():
    return {"message": "Welkom bij de JouwSong.nl API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
