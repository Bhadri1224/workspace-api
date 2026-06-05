from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Workspace(Base):
    __tablename__ = 'workspace'
    id = Column(Integer, primary_key=True)
    workspace_name = Column(String,nullable = False)
    description=Column(String,nullable = False)
    projects= relationship("Project", back_populates="workspace")
    summary=Column(String)
    status=Column(String)