from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api.endpoints import modules, quiz, progress

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Artificial Education API", version="1.0.0")

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For dev only, restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(modules.router, prefix="/api/modules", tags=["Modules"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Artificial Education API"}
