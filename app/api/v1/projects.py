from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.requests.project import ProjectCreate
from app.services.project import ProjectService

router = APIRouter(prefix="/workspaces", tags=["Projects"])

@router.post("/{workspace_id}/projects")
def add_project(
    workspace_id: int,
    project_schema: ProjectCreate,
    db: Session = Depends(get_db)
):
    return ProjectService.create_project(db, workspace_id, project_schema)

@router.get("/{workspace_id}/projects")
def get_workspace_projects(workspace_id: int, db: Session = Depends(get_db)):
    return ProjectService.fetch_workspace_projects(db, workspace_id)