"""

"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class PooolMemberships(Base):
    __tablename__ = "pool_memberships"

    id = Column(Integer, primary_key=True, index=True)
    pool_id = Column(Integer, ForeignKey("pools.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    role = Column(String(50), nullable=False)  # e.g., 'admin', 'member'
    joined_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)

    pool = relationship("Pool", back_populates="pool_memberships")
    user = relationship("User", back_populates="pool_memberships")