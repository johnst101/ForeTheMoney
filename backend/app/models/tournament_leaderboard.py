"""
Tournament Leaderboard model for storing tournament leaderboard data in the database.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Earnings(Base):
    __tablename__ = "earnings"

    orgId = Column(String(1), index=True, nullable=False)
    year = Column(String(4), index=True, nullable=False)
    tournId = Column(String(16), index=True, nullable=False)
    tournStatus = Column(String(32), nullable=False)
    roundId = Column(Integer, nullable=False)
    roundStatus = Column(String(32), nullable=False)
    lastUpdated = Column(DateTime, nullable=False)
    cutLine = Column(String(4), nullable=True)
    playerID = Column(String(16), index=True, nullable=False)
    tournPosition = Column(String(8), nullable=False)
    totalScore = Column(String(4), nullable=False)
    currentRoundScore = Column(String(4), nullable=False)
    roundComplete = Column(Boolean, default=False, nullable=False)
    thru = Column(String(4), nullable=False)
    teeTime = Column(DateTime, nullable=True)

    # TODO: Add relationships