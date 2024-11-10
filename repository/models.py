# db/models.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base
from constants import DEFAULT_LANGUAGE


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)
    language = Column(String, default=DEFAULT_LANGUAGE)


class RSSFeed(Base):
    __tablename__ = "rss_feeds"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rss_feeds")


User.rss_feeds = relationship(
    "RSSFeed", order_by=RSSFeed.id, back_populates="user", cascade="all, delete"
)
