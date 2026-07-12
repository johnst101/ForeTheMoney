"""
Pool leaderboard model for tracking user performance in pools.

Represents the leaderboard for a pool.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class PoolLeaderboards(Base):
    __tablename__ = "pool_leaderboards"

    year = Column(Integer, primary_key=True, index=True, nullable=False)
    pool_id = Column(Integer, ForeignKey("pools.id"), primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True, nullable=False)
    score = Column(Integer, nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pool = relationship("Pools", back_populates="pool_leaderboards")
    member = relationship("Users", back_populates="pool_leaderboards")