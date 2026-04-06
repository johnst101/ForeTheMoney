"""

"""

from ..db.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class PoolPicks(Base):
    __tablename__ = "pool_picks"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("pools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tournament_id = Column(Integer, ForeignKey("tournaments.id"), nullable=False)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    tier = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    week_number = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)

    pool = relationship("Pool", back_populates="picks")
    user = relationship("User", back_populates="picks")
    tournament = relationship("Tournament", back_populates="picks")
    player = relationship("Player", back_populates="picks")