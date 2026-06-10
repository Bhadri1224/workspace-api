# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth as api_auth, workspaces, projects
from app.auth import router as auth_router
from app.database import engine  # Added a dot to look in the current folder
from app.model import UserInfo,Base  # Added a dot to look in the current folder
import app.model as models       # This imports the models file so you can use models.Base
# Update line 7
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Modular Workspace Core Engine", version="1.0.0")

# 1. Frontend Cross-Origin Resource Sharing rules
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Adjust this to your React port (e.g., ["http://localhost:5173"])
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. Mount your clean enterprise domain routers
app.include_router(api_auth.router, prefix="/api/v1")
app.include_router(workspaces.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(auth_router)

@app.get("/")
def health_check():
    return {"status": "operational", "structure": "layered-architecture"}