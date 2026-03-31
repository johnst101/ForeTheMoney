from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Earnings(Base):
    __tablename__ = "earnings"

    year = Column(String, index=True, nullable=False)
    tournId = Column(String, index=True, nullable=False)
    playerID = Column(String, index=True, nullable=False)
    earnings = Column(Integer)
    timestamp = Column(DateTime, nullable=False)

    # TODO: Add relationships