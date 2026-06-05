from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.project import ProjectRepository
from app.repositories.workspace import WorkspaceRepository
from app.schemas.requests.project import ProjectCreate

class ProjectService:
    @staticmethod
    def create_project(db: Session, workspace_id: int, project_schema: ProjectCreate):
        # Constraint Check 1: Does the parent workspace cluster even exist?
        workspace = WorkspaceRepository.get_by_id(db, workspace_id)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace does not exist")

        # Constraint Check 2: Does this project identifier already exist inside THIS specific workspace?
        existing_project = ProjectRepository.get_project_in_workspace(
            db, workspace_id, project_schema.project_name
        )
        if existing_project:
            raise HTTPException(
                status_code=400,
                detail="Project already exists in this workspace"
            )

        # Execution
        return ProjectRepository.create(db, workspace_id, project_schema)

    @staticmethod
    def fetch_workspace_projects(db: Session, workspace_id: int):
        # Optional: verify workspace existence first if you want strict validation
        return ProjectRepository.get_all_by_workspace(db, workspace_id)