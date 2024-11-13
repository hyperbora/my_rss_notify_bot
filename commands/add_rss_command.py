from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from repository import rss_feed_repository, RSSFeed, User
from enums import UserStateEnum, CommandEnum, MessageEnum
from decorators import ensure_user_exists
from languages import get_translation
from constants import MAX_RSS_FEEDS

WAITING_FOR_URL = UserStateEnum.WAITING_FOR_URL


@ensure_user_exists
async def start_add_rss(update: Update, context: CallbackContext, user: User):
    await update.message.reply_text(get_translation(MessageEnum.PROMPT_ENTER_RSS_URL))
    return WAITING_FOR_URL


@ensure_user_exists
async def add_rss_url(update: Update, context: CallbackContext, user: User):
    # URL 입력값 받아오기
    rss_url = update.message.text.strip()

    # 이미 해당 사용자가 등록한 RSS 피드인지 확인
    existing_feed = rss_feed_repository.get_rss_by_url(rss_url, user)  # user 객체 전달

    if existing_feed:
        await update.message.reply_text(get_translation(MessageEnum.RSS_ALREADY_EXISTS))
        return ConversationHandler.END

    # 등록된 피드 개수 확인
    user_feed_count = len(rss_feed_repository.get_rss_feeds_by_user_id(user_id=user.id))
    if user_feed_count >= MAX_RSS_FEEDS:
        await update.message.reply_text(
            get_translation(
                MessageEnum.RSS_MAX_LIMIT, user.language, MAX_RSS_FEEDS=MAX_RSS_FEEDS
            )
        )
        return ConversationHandler.END

    # RSSFeed 객체 생성 후 저장
    rss_feed = RSSFeed(url=rss_url, user_id=user.id)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    if saved_feed:
        await update.message.reply_text(
            f"{get_translation(MessageEnum.SUCCESS_RSS_ADDED)}: {rss_url}"
        )
    else:
        await update.message.reply_text(
            get_translation(MessageEnum.ERROR_RSS_ADD_FAILED)
        )

    return ConversationHandler.END


async def cancel_rss_add(update: Update, context: CallbackContext):
    await update.message.reply_text(get_translation(MessageEnum.CANCEL_RSS_ADD))
    return ConversationHandler.END


add_rss_handler = ConversationHandler(
    entry_points=[CommandHandler(CommandEnum.ADD_RSS, start_add_rss)],
    states={
        WAITING_FOR_URL: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_rss_url)]
    },
    fallbacks=[CommandHandler(CommandEnum.CANCEL_RSS_ADD, cancel_rss_add)],
)
