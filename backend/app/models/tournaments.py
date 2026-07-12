"""
Tournament model for the PGA Tour tournaments from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Tournaments(Base):
    __tablename__ = "tournaments"

    org_id = Column(String(1), nullable=False)
    year = Column(String(4), nullable=False)
    tourn_id = Column(String(16), primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    purse = Column(Integer)
    fedex_cup_points = Column(Integer)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    week_number = Column(String(4))
    format = Column(String(200))
    status = Column(String(200))
    current_round = Column(Integer)
    time_zone = Column(String(200))
    course_id = Column(String(16))
    course_name = Column(String(200))
    country = Column(String(200))
    state = Column(String(200))
    city = Column(String(200))

    schedules = relationship("Schedules", back_populates="tournament")
    earnings = relationship("Earnings", back_populates="tournament")
    tournament_leaderboards = relationship("TournamentLeaderboard", back_populates="tournament")
    pool_picks = relationship("PoolPicks", back_populates="tournament")