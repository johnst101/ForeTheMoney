"""
Earnings model for storing player earnings data in the database.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Earnings(Base):
    __tablename__ = "earnings"

    year = Column(String(4), index=True, nullable=False)
    tournId = Column(String(16), index=True, nullable=False)
    playerID = Column(String(16), index=True, nullable=False)
    earnings = Column(Integer)
    timestamp = Column(DateTime, nullable=False)

    # TODO: Add relationships