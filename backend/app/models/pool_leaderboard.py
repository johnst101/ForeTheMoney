"""
Pool leaderboard model for tracking user performance in pools.

Represents the leaderboard for a pool.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class PoolLeaderboard(Base):
    __tablename__ = "pool_leaderboards"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    pool_id = Column(Integer, ForeignKey("pools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    score = Column(Integer, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # TODO: Add relationships