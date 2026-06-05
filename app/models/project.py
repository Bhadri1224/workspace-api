from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
#Table workspace Columns
class Project(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    workspace_id = Column(Integer, ForeignKey('workspace.id'))
    project_name=Column(String,nullable = False)
    description=Column(String,nullable = False)
    summary=Column(String)
    status = Column(String, default="pending")
    workspace=relationship("Workspace", back_populates="projects")
