"""

"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class PoolPicks(Base):
    __tablename__ = "pool_picks"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("pools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tourn_id = Column(String(16), ForeignKey("tournaments.tourn_id"), nullable=False)
    player_id = Column(String(16), ForeignKey("players.player_id"), nullable=False)
    tier = Column(Integer, nullable=False)
    year = Column(String(4), nullable=False)
    week_number = Column(String(4), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    pool = relationship("Pools", back_populates="pool_picks")
    member = relationship("Users", back_populates="pool_picks")
    tournament = relationship("Tournaments", back_populates="pool_picks")
    player = relationship("Players", back_populates="pool_picks")