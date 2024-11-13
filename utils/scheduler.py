import feedparser
from sqlalchemy.orm import Session
from repository.models import RSSFeed, RSSFeedHistory
from repository import user_repository, rss_feed_repository, get_db


def check_rss_feeds():
    # 모든 사용자에 대해
    with get_db() as db:
        for user in user_repository.get_all_users():
            # 사용자가 등록한 RSS 피드 가져오기
            rss_feeds = rss_feed_repository.get_rss_feeds_by_user_id(user_id=user.id)

            for rss_feed in rss_feeds:
                # RSS 피드 파싱
                feed = feedparser.parse(rss_feed.url)

                # 피드 항목 확인
                for entry in feed.entries:
                    # 각 RSS 항목에 대해 history를 확인하고, 없으면 추가
                    existing_history = (
                        db.query(RSSFeedHistory)
                        .filter(
                            RSSFeedHistory.rss_feed_id == rss_feed.id,
                            RSSFeedHistory.entry_id == entry.id,
                        )
                        .first()
                    )

                    # 새로운 항목이 없다면, history에 추가
                    if not existing_history:
                        new_history = RSSFeedHistory(
                            rss_feed_id=rss_feed.id,
                            entry_id=entry.id,
                            title=entry.title,
                            link=entry.link,
                            published=entry.published,
                        )
                        db.add(new_history)
                        db.commit()

                        # 여기서 알림을 보낼 수도 있음
                        send_notification_to_user(
                            user.chat_id, f"새 RSS 글: {entry.title}"
                        )


def send_notification_to_user(chat_id: str, message: str):
    # 여기에 Telegram bot 메시지 전송 기능을 구현
    print(f"send notification to {chat_id} : {message}")
    pass
