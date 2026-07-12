"""
Earnings model for storing player earnings data in the database.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

class Earnings(Base):
    __tablename__ = "earnings"

    year = Column(String(4), primary_key=True, index=True, nullable=False)
    tourn_id = Column(String(16), ForeignKey("tournaments.tourn_id"), primary_key=True, index=True, nullable=False)
    player_id = Column(String(16), ForeignKey("players.player_id"), primary_key=True, index=True, nullable=False)
    earnings = Column(Integer)
    timestamp = Column(DateTime, nullable=False)

    tournament = relationship("Tournaments", back_populates="earnings")
    player = relationship("Players", back_populates="earnings")