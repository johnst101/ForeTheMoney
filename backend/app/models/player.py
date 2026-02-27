"""
Player model for the PGA Tour players from the RapidAPI.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Player(Base):
    __tablename__ = "players"

    player_id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(200), nullable=False)
    last_name = Column(String(200), nullable=False)

    # TODO: Add relationships