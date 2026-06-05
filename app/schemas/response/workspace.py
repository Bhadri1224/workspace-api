from pydantic import BaseModel

class WorkspaceResponse(BaseModel):
    id: int
    workspace_name: str
    description: str | None = None
    summary: str | None = None

    # 🚨 Crucial config option: tells Pydantic to map fields directly from database objects
    model_config = {"from_attributes": True}