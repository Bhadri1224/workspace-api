from pydantic import BaseModel

class ProjectResponse(BaseModel):
    id: int
    project_name: str
    description: str
    summary: str | None = None
    workspace_id: int  # Tracking which workspace this project belongs to

    model_config = {"from_attributes": True}