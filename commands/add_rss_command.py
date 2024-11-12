from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from repository import rss_feed_repository, user_repository, RSSFeed
from enums import UserStateEnum, CommandEnum, MessageEnum
from decorators import ensure_user_exists
from languages import get_translation

WAITING_FOR_URL = UserStateEnum.WAITING_FOR_URL


@ensure_user_exists
async def start_add_rss(update: Update, context: CallbackContext):
    await update.message.reply_text(get_translation(MessageEnum.PROMPT_ENTER_RSS_URL))
    return WAITING_FOR_URL


@ensure_user_exists
async def add_rss_url(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    user = user_repository.get_user(chat_id=chat_id)

    # 사용자가 입력한 URL 가져오기
    rss_url = update.message.text

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
