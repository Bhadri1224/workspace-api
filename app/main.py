from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.models import Project
from app.schemas import WorkspaceCreate
from app.schemas import ProjectCreate
from app.crud import create_workspace
from app.crud import create_project
from app.database import Base, engine
from app.crud import get_workspace
from app.crud import delete_workspace
from app.schemas import UserCreate
from app.crud import create_user
from app.schemas import LoginRequest
from app.crud import login_user
from app.auth import get_current_user
from fastapi.security import OAuth2PasswordRequestForm
Base.metadata.create_all(bind=engine)
app = FastAPI()
# ─── 2. ADD THIS CORS MIDDLEWARE CONFIGURATION ───
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # Allows your Vite frontend port
    allow_credentials=True,
    allow_methods=["*"],                     # Allows GET, POST, PUT, DELETE
    allow_headers=["*"],                     # Allows Authorization & Content-Type headers
)
@app.get("/")
def home():
    return {"Workspace : running"}
@app.post("/workspaces")
def add_workspace(
    workspace: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return create_workspace(db, workspace)
@app.post("/workspaces/{workspace_id}/projects")
def add_project(workspace_id: int, project: ProjectCreate,db: Session = Depends(get_db)):
    return create_project(db, workspace_id, project)
@app.post("/register")
def register(user:UserCreate,db: Session = Depends(get_db)):
    return create_user(db, user)
@app.get("/workspaces/{workspace_id}")
def fetch_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return get_workspace(db, workspace_id)
@app.delete("/workspaces/{workspace_id}")
def remove_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return (delete_workspace(db, workspace_id))
@app.get("/workspaces/{workspace_id}/projects")
def get_workspace_projects(workspace_id: int, db: Session = Depends(get_db)):
    # 1. Query your Postgres DB for projects where workspace_id == workspace_id
    projects = db.query(Project).filter(Project.workspace_id == workspace_id).all()
    # 2. Return them as a list
    return projects
@app.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return login_user(db, form_data)