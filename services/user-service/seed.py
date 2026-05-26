import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, Base, engine
from app.models import User

Base.metadata.create_all(bind=engine)

USERS = [
    {"username": "alice", "email": "alice@example.com", "hashed_password": "hashed_secret"},
    {"username": "bob", "email": "bob@example.com", "hashed_password": "hashed_secret"},
    {"username": "charlie", "email": "charlie@example.com", "hashed_password": "hashed_secret"},
]

db = SessionLocal()
for u in USERS:
    exists = db.query(User).filter(User.email == u["email"]).first()
    if not exists:
        db.add(User(**u))
db.commit()
db.close()
print("Seeded users successfully.")