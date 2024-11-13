from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import feedparser
from repository.models import RSSFeedHistory
from repository import user_repository, rss_feed_repository, rss_feed_history_repository
from constants import RSS_CHECK_INTERVAL


def parse_published_at(date_str):
    for date_format in ["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%S%z"]:
        try:
            return datetime.strptime(date_str, date_format)
        except ValueError:
            continue
    raise ValueError("Unsupported date format")


# def delete_old_rss_history():
#     """
#     30일 이상 된 RSS 피드 기록을 삭제합니다.
#     """
#     cutoff_date = datetime.now() - timedelta(days=30)
#     with get_db() as db:
#         # 30일 이상 된 기록을 삭제
#         db.execute(
#             delete(RSSFeedHistory).where(RSSFeedHistory.published_at < cutoff_date)
#         )
#         db.commit()


def check_rss_feeds():
    # 모든 사용자에 대해

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
                    rss_feed_history_repository.get_entry_by_feed_and_entry_id(
                        rss_feed_id=rss_feed.id, entry_id=entry.id
                    )
                )

                # 새로운 항목이 없다면, history에 추가
                if not existing_history:
                    new_history = RSSFeedHistory(
                        rss_feed_id=rss_feed.id,
                        entry_id=entry.id,
                        title=entry.title,
                        link=entry.link,
                        published_at=parse_published_at(entry.published),
                    )
                    rss_feed_history_repository.save_entry(rss_feed_history=new_history)

                    # 여기서 알림을 보낼 수도 있음
                    send_notification_to_user(user.chat_id, f"새 RSS 글: {entry.title}")


def send_notification_to_user(chat_id: str, message: str):
    # 여기에 Telegram bot 메시지 전송 기능을 구현
    print(f"send notification to {chat_id} : {message}")


def start_rss_scheduler():
    """
    스케줄러를 시작하여 주기적으로 RSS를 확인합니다.
    """
    scheduler = BackgroundScheduler()
    interval_seconds = RSS_CHECK_INTERVAL

    # 주기적으로 check_rss_feeds 실행
    scheduler.add_job(
        check_rss_feeds,
        IntervalTrigger(seconds=interval_seconds),  # 환경변수에 따라 주기 설정
        next_run_time=datetime.now() + timedelta(seconds=interval_seconds),
        id="rss_check_job",  # 고유 ID 설정
    )

    scheduler.start()
