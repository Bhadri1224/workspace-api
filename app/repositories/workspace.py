from sqlalchemy.orm import Session
from app.models.workspace import Workspace
from app.schemas.requests.workspace import WorkspaceCreate

class WorkspaceRepository:
    @staticmethod
    def get_by_id(db: Session, workspace_id: int) -> Workspace | None:
        return db.query(Workspace).filter(Workspace.id == workspace_id).first()

    @staticmethod
    def get_by_name(db: Session, name: str) -> Workspace | None:
        return db.query(Workspace).filter(Workspace.workspace_name == name).first()

    @staticmethod
    def create(db: Session, schema: WorkspaceCreate) -> Workspace:
        obj = Workspace(
            workspace_name=schema.workspace_name,
            description=schema.description,
            summary=schema.summary
        )
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj

    @staticmethod
    def delete(db: Session, workspace: Workspace) -> None:
        db.delete(workspace)
        db.commit()