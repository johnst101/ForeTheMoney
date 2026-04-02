"""
Pool model for tracking user performance in pools.

Represents a pool of users who are competing against each other.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

class Pool(Base):
    __tablename__ = "pools"

    id = Column(Integer, primary_key=True, index=True)
    # TODO: Incomplete model - need to add fields for pool name, description, etc.