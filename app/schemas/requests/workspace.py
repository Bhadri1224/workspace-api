from pydantic import BaseModel

class WorkspaceCreate(BaseModel):
    workspace_name: str
    description: str
    summary: str | None = None