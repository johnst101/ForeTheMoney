"""
Tournament Leaderboard model for storing tournament leaderboard data in the database.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class TournamentLeaderboard(Base):
    __tablename__ = "tournament_leaderboard"

    org_id = Column(String(1), index=True, nullable=False)
    year = Column(String(4), primary_key=True, index=True, nullable=False)
    tourn_id = Column(String(16), ForeignKey("tournaments.tourn_id"), primary_key=True, index=True, nullable=False)
    tourn_status = Column(String(32), nullable=False)
    round_id = Column(Integer, primary_key=True, index=True, nullable=False)
    round_status = Column(String(32), nullable=False)
    last_updated = Column(DateTime, nullable=False)
    cut_line = Column(String(4), nullable=True)
    player_id = Column(String(16), ForeignKey("players.player_id"), primary_key=True, index=True, nullable=False)
    tourn_position = Column(String(8), nullable=False)
    total_score = Column(String(4), nullable=False)
    current_round_score = Column(String(4), nullable=False)
    round_complete = Column(Boolean, default=False, nullable=False)
    thru = Column(String(4), nullable=False)
    tee_time = Column(DateTime, nullable=True)

    player = relationship("Players", back_populates="tournament_leaderboards")
    tournament = relationship("Tournaments", back_populates="tournament_leaderboards")