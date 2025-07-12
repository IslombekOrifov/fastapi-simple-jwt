from typing import Optional
from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime, Boolean, Index
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    __table_args__ = (
        Index('ix_refresh_tokens_token', 'token', 
             comment='Index for fast token lookup'),
        Index('ix_refresh_tokens_user_token', 'user_id', 'token',
             comment='Composite index for user token sessions'),
    )
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    token: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    device_name = mapped_column(String, nullable=False)
    fingerprint_hash = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        comment='Token creation timestamp'
    )
    expires_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), comment='Token expiration timestamp'
    )
    revoked: Mapped[bool] = mapped_column(
        Boolean, default=False, comment='Is token revoked'
    )