from sqlalchemy.orm import Session
from app.models.project import Project
from app.schemas.requests.project import ProjectCreate

class ProjectRepository:
    @staticmethod
    def get_project_in_workspace(db: Session, workspace_id: int, project_name: str) -> Project | None:
        return db.query(Project).filter(
            Project.workspace_id == workspace_id,
            Project.project_name == project_name
        ).first()

    @staticmethod
    def get_all_by_workspace(db: Session, workspace_id: int) -> list[Project]:
        return db.query(Project).filter(Project.workspace_id == workspace_id).all()

    @staticmethod
    def create(db: Session, workspace_id: int, schema: ProjectCreate) -> Project:
        obj = Project(
            workspace_id=workspace_id,
            project_name=schema.project_name,
            description=schema.description,
            summary=schema.summary
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj