"""
Player model for the PGA Tour players from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Players(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)

    earnings = relationship("Earnings", back_populates="player")
    pool_picks = relationship("PoolPicks", back_populates="player")