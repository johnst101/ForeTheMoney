"""
User model for authentication and user management.

Represents users in the ForeTheMoney web app with email/password authentication.
Supports soft deletes via is_active.
"""

from ..db.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    phone_number = Column(String(10), nullable=True)
    email = Column(String(120), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_active = Column(Boolean, default=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    pools = relationship("Pools", back_populates="owner", cascade="all, delete-orphan")
    pool_memberships = relationship("PoolMemberships", back_populates="member", cascade="all, delete-orphan")
    pool_picks = relationship("PoolPicks", back_populates="member", cascade="all, delete-orphan")
    pool_leaderboards = relationship("PoolLeaderboards", back_populates="member", cascade="all, delete-orphan")