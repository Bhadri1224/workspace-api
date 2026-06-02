from fastapi import FastAPI
from fastapi import Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas import WorkspaceCreate
from app.schemas import ProjectCreate
from app.crud import create_workspace
from app.crud import create_project
from app.database import Base, engine
from app.crud import get_workspace
from app.models import Workspace
from app.crud import delete_workspace
Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.get("/")
def home():
    return {"Workspace : running"}
@app.post("/workspaces")
def add_workspace(workspace: WorkspaceCreate,db: Session = Depends(get_db)):
    return create_workspace(db, workspace)
@app.post("/workspaces/{workspace_id}/projects")
def add_project(workspace_id: int, project: ProjectCreate,db: Session = Depends(get_db)):
    return create_project(db, workspace_id, project)
@app.get("/workspaces/{workspace_id}")
def fetch_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return get_workspace(db, workspace_id)
@app.delete("/workspaces/{workspace_id}")
def remove_workspace(
    workspace_id: int,
    db: Session = Depends(get_db)
):
    return delete_workspace(db, workspace_id)