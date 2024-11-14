from datetime import datetime, timedelta
from repository import get_db
from repository.models import RSSFeedHistory


def get_entry_by_feed_and_entry_id(rss_feed_id: int, entry_id: str) -> RSSFeedHistory:
    """
    특정 RSS 피드와 엔트리 ID로 RSSFeedHistory 레코드를 조회합니다.
    """
    with get_db() as db:
        return (
            db.query(RSSFeedHistory)
            .filter(
                RSSFeedHistory.rss_feed_id == rss_feed_id,
                RSSFeedHistory.entry_id == entry_id,
            )
            .first()
        )


def save_entry(rss_feed_history: RSSFeedHistory) -> RSSFeedHistory:
    """
    새로운 RSSFeedHistory 레코드를 데이터베이스에 저장합니다.
    """
    with get_db() as db:
        db.add(rss_feed_history)
        db.commit()
        db.refresh(rss_feed_history)
        return rss_feed_history


def delete_old_entries(rss_feed_id: int, keep_last: int = 10):
    """
    주어진 RSS 피드의 오래된 엔트리 기록을 삭제하여 최신 기록만 유지합니다.
    """
    with get_db() as db:
        subquery = (
            db.query(RSSFeedHistory.id)
            .filter(RSSFeedHistory.rss_feed_id == rss_feed_id)
            .order_by(RSSFeedHistory.timestamp.desc())
            .limit(keep_last)
            .subquery()
        )
        db.query(RSSFeedHistory).filter(
            RSSFeedHistory.rss_feed_id == rss_feed_id, ~RSSFeedHistory.id.in_(subquery)
        ).delete(synchronize_session=False)
        db.commit()


def delete_old_rss_history(days: int = 30):
    """
    days 이상 된 RSS 피드 기록을 삭제합니다.
    """
    cutoff_date = datetime.now() - timedelta(days=days)
    with get_db() as db:
        db.execute(
            db.delete(RSSFeedHistory).where(RSSFeedHistory.published_at < cutoff_date)
        )
        db.commit()
