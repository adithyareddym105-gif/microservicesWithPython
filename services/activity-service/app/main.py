from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx
from app.database import Base, engine, get_db
from app.models import Activity
from app.schemas import ActivityCreate, ActivityOut
from app.infrastructure.rabbitmq_publisher import publish_notification

Base.metadata.create_all(bind=engine)
app = FastAPI()

USER_SERVICE_URL = "http://localhost:8001"
GAME_SERVICE_URL = "http://localhost:8002"

async def validate_user(user_id: int) -> dict:
    for attempt in range(2):
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(f"{USER_SERVICE_URL}/v1/users/{user_id}")
                if resp.status_code == 404:
                    raise HTTPException(status_code=404, detail=f"User {user_id} not found")
                resp.raise_for_status()
                return resp.json()
        except HTTPException:
            raise
        except httpx.RequestError:
            if attempt == 1:
                raise HTTPException(status_code=503, detail="User service unavailable")

async def fetch_game(game_id: int):
    if game_id is None:
        return None
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{GAME_SERVICE_URL}/v1/games/{game_id}")
            if resp.status_code == 200:
                return resp.json()
            return None
    except Exception:
        return None

@app.post("/v1/activities", response_model=ActivityOut)
async def create_activity(data: ActivityCreate, db: Session = Depends(get_db)):
    await validate_user(data.user_id)
    activity = Activity(user_id=data.user_id, game_id=data.game_id, action=data.action)
    db.add(activity)
    db.commit()
    db.refresh(activity)

    publish_notification({
        "user_id": activity.user_id,
        "message": f"User {activity.user_id} performed action: {activity.action}",
        "game_id": activity.game_id,
        "activity_id": activity.id
    })

    game = await fetch_game(data.game_id)
    result = ActivityOut.model_validate(activity)
    result.game = game
    return result

@app.get("/v1/activities", response_model=list[ActivityOut])
def list_activities(db: Session = Depends(get_db)):
    return db.query(Activity).all()

@app.get("/")
def root():
    return {"message": "Activity service running"}
