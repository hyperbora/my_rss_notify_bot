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

    def __str__(self):
        # 사람이 읽기 쉬운 형태로 출력
        return f"User(id={self.id}, chat_id={self.chat_id}, language={self.language})"

    def __repr__(self):
        # 디버깅용, 개발자에게 더 많은 정보를 제공
        return f"User(id={self.id}, chat_id={self.chat_id}, language={self.language})"


class RSSFeed(Base):
    __tablename__ = "rss_feeds"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rss_feeds")


User.rss_feeds = relationship(
    "RSSFeed", order_by=RSSFeed.id, back_populates="user", cascade="all, delete"
)


class RSSFeedHistory(Base):
    __tablename__ = "rss_feed_history"
    id = Column(Integer, primary_key=True)
    rss_feed_id = Column(Integer, ForeignKey("rss_feeds.id"))
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    published_at = Column(String, nullable=False)

    rss_feed = relationship("RSSFeed", back_populates="history")


RSSFeed.history = relationship(
    "RSSFeedHistory",
    order_by=RSSFeedHistory.id,
    back_populates="rss_feed",
    cascade="all, delete",
)
