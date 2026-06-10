from sqlalchemy import Column, Integer, String, DateTime
from app.database import Base
import datetime


class UserInfo(Base):
    __tablename__ = "user_info"  # Table name in Postgres

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)  # Remember to store hashed passwords here

    # Tracking session details
    last_login = Column(DateTime, nullable=True)
    last_logout = Column(DateTime, nullable=True)
class SessionHistory(Base):
    __tablename__ = "session_history"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    time_in = Column(DateTime)
    time_out = Column(DateTime)
    duration = Column(String)