from fastapi import FastAPI
from pydantic import BaseModel

# Import all models to ensure relationships are registered
from app.models.users import Users
from app.models.pools import Pools
from app.models.pool_memberships import PoolMemberships
from app.models.pool_picks import PoolPicks
from app.models.pool_leaderboards import PoolLeaderboards
from app.models.tournaments import Tournaments
from app.models.schedules import Schedules
from app.models.earnings import Earnings
from app.models.player import Players
from app.models.tournament_leaderboard import TournamentLeaderboard

from app.routes.auth import auth_router

app = FastAPI()

app.include_router(auth_router)

@app.get("/")
def read_root():
    return {"Hello": "World"}