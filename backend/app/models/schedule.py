"""
Schedule model for the PGA Tour schedule from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False, index=True)
    org_id = Column(Integer, nullable=False)
    tourn_id = Column(Integer, nullable=False, index=True)
    name = Column(String, nullable=False)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    week_number = Column(Integer, nullable=False, index=True)
    purse = Column(Integer, nullable=False)
    winners_share = Column(Integer)

    # TODO: Add relationships