from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .db import Base
from constants import DEFAULT_LANGUAGE


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    chat_id = Column(String, unique=True)
    language = Column(String, default=DEFAULT_LANGUAGE)

    def __str__(self):
        return f"User(id={self.id}, chat_id={self.chat_id}, language={self.language})"

    def __repr__(self):
        return f"User(id={self.id}, chat_id={self.chat_id}, language={self.language})"


class RSSFeed(Base):
    __tablename__ = "rss_feeds"
    id = Column(Integer, primary_key=True)
    url = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="rss_feeds")

    def __repr__(self):
        return f"RSSFeed(id={self.id}, url={self.url}, user_id={self.user_id})"


User.rss_feeds = relationship(
    "RSSFeed", order_by=RSSFeed.id, back_populates="user", cascade="all, delete"
)


class RSSFeedHistory(Base):
    __tablename__ = "rss_feed_histories"
    id = Column(Integer, primary_key=True)
    rss_feed_id = Column(Integer, ForeignKey("rss_feeds.id"))
    entry_id = Column(String, nullable=False)  # RSS 항목의 고유 ID 저장
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    published_at = Column(DateTime, nullable=False)  # 날짜 형식으로 변경

    rss_feed = relationship("RSSFeed", back_populates="rss_feed_histories")

    def __repr__(self):
        return f"RSSFeedHistory(id={self.id}, rss_feed_id={self.rss_feed_id}, entry_id={self.entry_id})"


RSSFeed.rss_feed_histories = relationship(
    "RSSFeedHistory",
    order_by=RSSFeedHistory.id,
    back_populates="rss_feed",
    cascade="all, delete",
)
