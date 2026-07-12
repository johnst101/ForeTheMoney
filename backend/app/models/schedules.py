"""
Schedule model for the PGA Tour schedule from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

class Schedules(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(String(4), nullable=False, index=True)
    org_id = Column(String(1), nullable=False)
    tourn_id = Column(String(16), ForeignKey("tournaments.tourn_id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    week_number = Column(String(4), nullable=False, index=True)
    purse = Column(Integer, nullable=False)
    winners_share = Column(Integer)

    tournament = relationship("Tournaments", back_populates="schedules")