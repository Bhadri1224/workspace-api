from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.workspace import WorkspaceRepository
from app.schemas.requests.workspace import WorkspaceCreate
from app.repositories.audit_log import AuditLogRepository

class WorkspaceService:
    @staticmethod
    def create_workspace(db: Session, workspace_schema: WorkspaceCreate,current_user:str):
        # Rule: Check if name is already taken
        existing_workspace = WorkspaceRepository.get_by_name(db, workspace_schema.workspace_name)
        if existing_workspace:
            raise HTTPException(status_code=400, detail="Workspace already exists")


        # Delegate raw DB save to Repository
        new_workspace= WorkspaceRepository.create(db, workspace_schema)
        # 2. 🛡️ Write to the Audit Log right after a successful database save!
        AuditLogRepository.log_event(
            db=db,
            username=current_user,
            action="CREATE_WORKSPACE",
            resource=f"Workspace: {new_workspace.workspace_name} (ID: {new_workspace.id})",
            extra={"description": new_workspace.description}
        )
        return new_workspace

    @staticmethod
    def get_workspace(db: Session, workspace_id: int):
        workspace = WorkspaceRepository.get_by_id(db, workspace_id)
        if not workspace:
            raise HTTPException(status_code=404, detail="Workspace does not exist")
        return workspace

    @staticmethod
    def delete_workspace(db: Session, workspace_id: int,current_user:str):
        workspace = WorkspaceRepository.get_by_id(db, workspace_id)
        workspace_name=workspace.workspace_name
        WorkspaceRepository.delete(db, workspace)
        AuditLogRepository.log_event(
            db=db,
            username=current_user,
            action="DELETE_WORKSPACE",
            resource=f"Workspace: {workspace_name} (ID: {workspace_id})"
        )

        # 4. Return response to the router layer
        return {"message": "Workspace deleted successfully"}