# Infrastructure layer — ORM model.
#
# This is the only file that defines the shape of the `users` table.
# It maps Python attributes to database columns using SQLAlchemy.
#
# This file should:
# - Import Base from app.database
# - Define a User class with columns: id, username, email,
#   hashed_password, is_active, created_at
#
# Rule: no business logic here. This file only describes data structure.
#
# See the README for the full implementation.
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())