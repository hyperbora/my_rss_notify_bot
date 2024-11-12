from typing import Optional, List
from repository import get_db
from repository.models import RSSFeed, User


def save_rss_feed(rss_feed: RSSFeed) -> RSSFeed:
    """
    RSS 피드를 저장합니다. 기존 피드가 없으면 새로 추가하고, 있으면 업데이트합니다.
    """
    with get_db() as db:
        db.add(rss_feed)
        db.commit()
        db.refresh(rss_feed)
        return rss_feed


def delete_rss_feed(rss_feed_id: int) -> bool:
    """
    주어진 ID를 가진 RSS 피드를 삭제합니다. 성공적으로 삭제되면 True를 반환합니다.
    """
    with get_db() as db:
        rss_feed = db.query(RSSFeed).filter(RSSFeed.id == rss_feed_id).first()
        if rss_feed:
            db.delete(rss_feed)
            db.commit()
            return True
    return False


def get_rss_feed(rss_feed_id: int) -> Optional[RSSFeed]:
    """
    주어진 ID를 가진 RSS 피드를 반환합니다.
    """
    with get_db() as db:
        return db.query(RSSFeed).filter(RSSFeed.id == rss_feed_id).first()


def get_rss_feeds_by_user_id(user_id: int) -> List[RSSFeed]:
    """
    특정 사용자 ID와 연결된 모든 RSS 피드를 반환합니다.
    """
    with get_db() as db:
        return db.query(RSSFeed).filter(RSSFeed.user_id == user_id).all()


def get_rss_by_url(rss_url: str, user: User) -> Optional[RSSFeed]:
    with get_db() as db:
        return (
            db.query(RSSFeed)
            .filter(RSSFeed.url == rss_url, RSSFeed.user_id == user.id)
            .first()
        )
