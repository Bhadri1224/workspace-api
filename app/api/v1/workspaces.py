from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.services.auth import get_current_user
from app.schemas.requests.workspace import WorkspaceCreate
from app.services.workspace import WorkspaceService
from app.schemas.requests.workspace import WorkspaceCreate
from app.schemas.response.workspace import WorkspaceResponse
router = APIRouter(prefix="/workspaces", tags=["Workspaces"])

@router.post("/workspaces", response_model=WorkspaceResponse)
def add_workspace(
    workspace_schema: WorkspaceCreate,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    return WorkspaceService.create_workspace(db, workspace_schema,current_user)

@router.get("/{workspace_id}")
def fetch_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return WorkspaceService.get_workspace(db, workspace_id)

@router.delete("/{workspace_id}")
def remove_workspace(workspace_id: int, db: Session = Depends(get_db)):
    return WorkspaceService.delete_workspace(db, workspace_id)