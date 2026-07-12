"""

"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class PoolMemberships(Base):
    __tablename__ = "pool_memberships"

    pool_id = Column(Integer, ForeignKey("pools.id"), primary_key=True, index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True, index=True, nullable=False)
    role = Column(String(50), nullable=False)  # e.g., 'admin', 'member'
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    pool = relationship("Pools", back_populates="pool_memberships")
    member = relationship("Users", back_populates="pool_memberships")