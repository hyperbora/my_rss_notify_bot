from typing import List
from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from repository import rss_feed_repository, rss_feed_history_repository, User, RSSFeed
from enums import CommandEnum, MessageEnum
from decorators import ensure_user_exists
from languages import get_translation
from utils import log_util, get_rss_feed_info, format_date_for_user

logger = log_util.logger


def format_rss_list(rss_feeds: List[RSSFeed], user: User):
    """RSS 피드 목록을 포맷된 문자열로 반환합니다."""
    rss_list = f"{get_translation(MessageEnum.REGISTERED_RSS_FEED_LIST, language=user.language)}:\n\n"
    for i, feed in enumerate(rss_feeds, start=1):
        last_update = rss_feed_history_repository.get_latest_entry_date(feed.id)
        last_update_str = (
            format_date_for_user(last_update, user.language)
            if last_update
            else get_translation(
                MessageEnum.NO_UPDATE_INFORMATION, language=user.language
            )
        )

        title, url = get_rss_feed_info(feed.url)

        last_update_label = get_translation(
            MessageEnum.LAST_UPDATED, language=user.language
        )

        rss_list += (
            f"{i}. {title}\n"
            f"- URL: {url}\n"
            f"- {last_update_label}: {last_update_str}\n\n"
        )
    return rss_list


@ensure_user_exists
async def show_rss_command(update: Update, context: CallbackContext, user: User):
    try:
        # 사용자가 등록한 RSS 피드 가져오기
        rss_feeds = rss_feed_repository.get_rss_feeds_by_user_id(user_id=user.id)

        # RSS 피드 목록 형식화
        if rss_feeds:
            message = format_rss_list(rss_feeds, user)
        else:
            message = get_translation(
                MessageEnum.NO_RSS_FEEDS_REGISTERED, user.language
            )

        await update.message.reply_text(message)

    except Exception as e:
        logger.error("Error at show_rss_command", exc_info=True)
        await update.message.reply_text(
            get_translation(
                MessageEnum.ERROR_FETCHING_RSS_FEEDS, language=user.language
            )
        )


show_rss_command_handler = CommandHandler(CommandEnum.SHOW_RSS, show_rss_command)
