from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models import Workspace
from app.models import Project
def create_workspace(db, workspace):
    existing_workspace=(
        db.query(Workspace)
        .filter(Workspace.workspace_name==workspace.workspace_name)
        .first()
    )
    if existing_workspace:
        raise HTTPException(status_code=400, detail="Workspace already exists")

    obj = Workspace(workspace_name=workspace.workspace_name,description=workspace.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
# exception handling


def create_project(db:Session,workspace_id: int,project):
    workspace=(db.query(Workspace).filter(Workspace.id==workspace_id).first())
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace does not exist")
    existing_project = (
        db.query(Project)
        .filter(
            Project.workspace_id == workspace_id,
            Project.project_name == project.project_name
        )
        .first()
    )
    if existing_project:
        raise HTTPException(
            status_code=400,
            detail="Project already exists in this workspace"
        )
    obj=Project(workspace_id=workspace_id,project_name=project.project_name,description=project.description)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
#GET
def get_workspace(db: Session, workspace_id: int):
    workspace=(
        db.query(Workspace)
        .filter(Workspace.id==workspace_id)
        .first()
    )
    if not workspace:
        raise HTTPException(status_code=404, detail="Workspace does not exist")
    return workspace
#DELETE
def delete_workspace(db: Session, workspace_id: int):
    workspace = (
        db.query(Workspace)
        .filter(Workspace.id == workspace_id)
        .first()
    )

    if not workspace:
        raise HTTPException(
            status_code=404,
            detail="Workspace does not exist"
        )

    db.delete(workspace)
    db.commit()

    return {"message": "Workspace deleted successfully"}