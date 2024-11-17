from typing import List
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler
from enums import RssFeedDeleteActionEnum, CommandEnum, MessageEnum
from languages import get_translation
from repository import rss_feed_repository, User, RSSFeed
from decorators import ensure_user_exists


# 사용자가 선택한 RSS를 삭제하는 함수
@ensure_user_exists
async def delete_rss_command(update: Update, context: CallbackContext, user: User):
    rss_feeds: List[RSSFeed] = rss_feed_repository.get_rss_feeds_by_user_id(user.id)

    if not rss_feeds:
        await update.message.reply_text(
            get_translation(MessageEnum.NO_RSS_TO_DELETE, user.language)
        )
        return

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{rss_feed.title} - {rss_feed.url}",
                callback_data=f"{CommandEnum.DELETE_RSS.value}:{rss_feed.id}",
            )
        ]
        for rss_feed in rss_feeds
    ]

    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text(
        f"{get_translation(MessageEnum.SELECT_RSS_TO_DELETE, user.language)}:",
        reply_markup=reply_markup,
    )


# 삭제 확인 단계
@ensure_user_exists
async def confirm_delete_rss(update: Update, context: CallbackContext, user: User):
    query = update.callback_query
    data = query.data

    if data.startswith(f"{CommandEnum.DELETE_RSS.value}:"):
        feed_id = int(data.split(":")[1])

        # "예"와 "아니오" 버튼 생성
        buttons = [
            [
                InlineKeyboardButton(
                    get_translation(MessageEnum.CONFIRM_YES, user.language),
                    callback_data=f"{RssFeedDeleteActionEnum.CONFIRM.value}:{feed_id}",
                ),
                InlineKeyboardButton(
                    get_translation(MessageEnum.CONFIRM_NO, user.language),
                    callback_data=RssFeedDeleteActionEnum.CANCEL.value,
                ),
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)
        await query.answer()
        await query.edit_message_text(
            text=get_translation(MessageEnum.CONFIRM_DELETE_RSS, user.language),
            reply_markup=reply_markup,
        )


# 삭제 처리 및 취소
@ensure_user_exists
async def handle_confirmation(update: Update, context: CallbackContext, user: User):
    query = update.callback_query
    data = query.data

    if data.startswith(RssFeedDeleteActionEnum.CONFIRM.value):
        feed_id = int(data.split(":")[1])
        rss_feed_repository.delete_rss_feed(feed_id)  # 삭제 처리

        await query.answer(
            get_translation(MessageEnum.RSS_DELETED_SUCCESS, user.language)
        )
        await query.edit_message_text(
            get_translation(MessageEnum.RSS_DELETED_CONFIRM, user.language)
        )

    elif data == RssFeedDeleteActionEnum.CANCEL.value:
        await query.answer(
            get_translation(MessageEnum.DELETE_OPERATION_CANCELED, user.language)
        )
        await query.edit_message_text(
            get_translation(MessageEnum.DELETE_CANCELED, user.language)
        )


delete_rss_command_handler = CommandHandler(
    f"{CommandEnum.DELETE_RSS.value}", delete_rss_command
)
confirm_delete_rss_callback_query_handler = CallbackQueryHandler(
    confirm_delete_rss, pattern=f"^{CommandEnum.DELETE_RSS.value}:"
)
handle_confirm_delete_callback_query_handler = CallbackQueryHandler(
    handle_confirmation,
    pattern=f"^{RssFeedDeleteActionEnum.CONFIRM.value}|{RssFeedDeleteActionEnum.CANCEL.value}$",
)
