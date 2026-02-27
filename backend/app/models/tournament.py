"""
Tournament model for the PGA Tour tournaments from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

class Tournament(Base):
    __tablename__ = "tournaments"

    org_id = Column(Integer, nullable=False)
    year = Column(Integer)
    tourn_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    purse = Column(Integer)
    fedex_cup_points = Column(Integer)
    start = Column(DateTime, nullable=False)
    end = Column(DateTime, nullable=False)
    week_number = Column(Integer)
    format = Column(String(200))
    status = Column(String(200))
    current_round = Column(Integer)
    time_zone = Column(String(200))
    course_id = Column(Integer)
    course_name = Column(String(200))
    country = Column(String(200))
    state = Column(String(200))
    city = Column(String(200))