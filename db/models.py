from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from typing import Optional
from datetime import datetime


class Base(DeclarativeBase):
    pass


class Artists(Base):
    __tablename__ = "artists"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)


class YouTubeArtists(Base):
    __tablename__ = "youtube_artists"

    youtube_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    youtube_channel_id: Mapped[str] = mapped_column(nullable=False, unique=True)
    artist_name: Mapped[Optional[str]] = mapped_column(nullable=True)


class YouTubeArtistStats(Base):
    __tablename__ = "youtube_artist_stats"

    youtube_id: Mapped[int] = mapped_column(
        ForeignKey("youtube_artists.youtube_id", ondelete="CASCADE"),
        primary_key=True,
    )
    date_pulled: Mapped[datetime] = mapped_column(primary_key=True)
    subscriber_count: Mapped[int] = mapped_column(nullable=False)
    view_count: Mapped[int] = mapped_column(nullable=False)


class Users(Base):
    __tablename__ = "users"
    user_id: Mapped[str] = mapped_column(primary_key=True)
    hashed_pass: Mapped[str] = mapped_column(nullable=False)


class AuthSessions(Base):
    __tablename__ = "auth_sessions"
    session_id: Mapped[str] = mapped_column(primary_key=True)
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(nullable=False)
    expiry: Mapped[datetime] = mapped_column(nullable=False)
    ip_address: Mapped[Optional[str]] = mapped_column(nullable=True)
