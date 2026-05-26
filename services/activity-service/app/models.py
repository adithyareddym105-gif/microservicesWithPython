from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    game_id = Column(Integer, nullable=True)
    action = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())