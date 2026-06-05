# app/models/audit_log.py
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, JSON
from app.database import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=False)                    # Who did it
    action = Column(String, index=True, nullable=False)                      # What they did (e.g., 'CREATE_WORKSPACE')
    resource = Column(String, nullable=False)                                # Target asset name/ID
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))   # When (UTC time)
    ip_address = Column(String, nullable=True)                               # Network origin IP
    extra_details = Column(JSON, nullable=True)                              # Extra metadata dict