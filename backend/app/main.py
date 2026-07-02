from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.core.migrations import ensure_runtime_columns
from app.api.endpoints import admin, auth, gamification, modules, progress, quiz, recommendation

# Create DB Tables
Base.metadata.create_all(bind=engine)
ensure_runtime_columns(engine)

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
app.include_router(auth.router, prefix="/api/auth", tags=["Auth"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(gamification.router, prefix="/api/gamification", tags=["Gamification"])
app.include_router(modules.router, prefix="/api/modules", tags=["Modules"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(recommendation.router, prefix="/api/recommendation", tags=["Recommendation"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Artificial Education API"}
