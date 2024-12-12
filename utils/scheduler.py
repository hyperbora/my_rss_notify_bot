from datetime import datetime, timedelta
from collections import OrderedDict
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import feedparser
from telegram import Bot
from telegram.error import TelegramError
from repository.models import RSSFeedHistory, RSSFeed
from repository import user_repository, rss_feed_repository, rss_feed_history_repository
from constants import RSS_CHECK_INTERVAL, OLD_RSS_HISTORY_DAYS, BOT_TOKEN
from utils import log_util
from enums import MessageEnum


logger = log_util.logger


def parse_published_at(date_str: str):
    for date_format in [
        "%a, %d %b %Y %H:%M:%S %z",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%d",
        "%Y%m%d",
        "%Y-%m-%d %H:%M:%S",
    ]:
        try:
            return datetime.strptime(date_str.strip(), date_format)
        except ValueError:
            continue
    logger.debug("unknown pattern : %s", date_str)
    return datetime.now()


def delete_old_rss_history():
    logger.info("delete_old_rss_history start")
    rss_feed_history_repository.delete_old_rss_history(days=OLD_RSS_HISTORY_DAYS)


async def check_rss_feeds():
    logger.info("check_rss_feeds scheduler start.")
    # 모든 사용자에 대해
    for user in user_repository.get_all_users():
        # 사용자가 등록한 RSS 피드 가져오기
        rss_feeds = rss_feed_repository.get_rss_feeds_by_user_id(user_id=user.id)

        new_entries_summary = OrderedDict()

        for rss_feed in rss_feeds:
            # RSS 피드 파싱
            feed = feedparser.parse(rss_feed.url)

            # 피드 항목 확인
            for entry in feed.entries:
                try:
                    # 각 RSS 항목에 대해 history를 확인하고, 없으면 추가
                    title = entry.get("title")
                    link = entry.get("link")
                    entry_id = entry.get("id", link)
                    published_at = (
                        entry.get("published")
                        or entry.get("updated")
                        or entry.get("pubDate")
                        or entry.get("wDate")
                        or ""
                    )
                    existing_history = (
                        rss_feed_history_repository.get_entry_by_feed_and_entry_id(
                            rss_feed_id=rss_feed.id, entry_id=entry_id
                        )
                    )

                    # 새로운 항목이 없다면, history에 추가
                    if not existing_history:
                        new_history = RSSFeedHistory(
                            rss_feed_id=rss_feed.id,
                            entry_id=entry_id,
                            title=title,
                            link=link,
                            published_at=parse_published_at(published_at),
                        )
                        rss_feed_history_repository.save_entry(
                            rss_feed_history=new_history
                        )

                        # 새로운 항목을 요약 정보에 추가
                        if rss_feed not in new_entries_summary:
                            new_entries_summary[rss_feed] = []
                        new_entries_summary[rss_feed].append(entry)
                except Exception:
                    logger.error(
                        "User(%s), URL(%s)", user.id, rss_feed.url, exc_info=True
                    )

        # 사용자에게 보낼 요약 메시지 생성
        if new_entries_summary:
            message = create_rss_update_message(new_entries_summary, user.language)
            # 요약 메시지를 사용자에게 전송
            await send_notification_to_user(user.chat_id, message)


def create_rss_update_message(new_entries_summary: dict[RSSFeed, list], language):
    """
    새로운 RSS 항목들을 요약해서 메시지로 변환하는 함수
    """
    from languages import get_translation

    message = f"{get_translation(MessageEnum.NEW_RSS_UPDATES, language)}\n\n"

    for rss_feed, entries in new_entries_summary.items():
        message += (
            f"{get_translation(MessageEnum.SOURCE, language)}: {rss_feed.title}\n\n"
        )
        for entry in entries[:2]:  # 최신 2개 항목만 표시
            message += f"- {entry.title} - [Link]({entry.link})\n\n"
        if len(entries) > 2:
            more_updates = get_translation(
                MessageEnum.MORE_UPDATES, language, SIZE=len(entries) - 2
            )
            message += f"{more_updates}\n\n"

    message += get_translation(MessageEnum.CLICK_TO_VIEW, language)
    return message


async def send_notification_to_user(chat_id: str, message: str):
    """
    텔레그램 사용자에게 메시지를 보내는 함수.
    chat_id: 사용자의 고유 텔레그램 ID
    message: 보낼 메시지
    """
    bot = Bot(token=BOT_TOKEN)
    try:
        # 메시지 전송
        await bot.send_message(chat_id=chat_id, text=message)
    except TelegramError as e:
        logger.error("메시지 전송 중 오류 발생", exc_info=True)


def start_rss_scheduler():
    """
    스케줄러를 시작하여 주기적으로 오래된 history 삭제 및 신규 rss를 확인합니다.
    """
    scheduler_cleanup = BackgroundScheduler()
    scheduler_cleanup.add_job(
        delete_old_rss_history,
        "interval",
        days=1,
        next_run_time=datetime.now() + timedelta(seconds=60),
        id="delete_rss_history_job",  # 고유 ID 설정
    )

    interval_seconds = RSS_CHECK_INTERVAL

    scheduler_notifications = AsyncIOScheduler()
    # 주기적으로 check_rss_feeds 실행
    scheduler_notifications.add_job(
        check_rss_feeds,
        IntervalTrigger(seconds=interval_seconds),  # 환경변수에 따라 주기 설정
        next_run_time=datetime.now() + timedelta(seconds=120),
        id="rss_check_job",  # 고유 ID 설정
    )

    scheduler_cleanup.start()
    scheduler_notifications.start()
