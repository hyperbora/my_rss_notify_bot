from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler, CallbackContext, CallbackQueryHandler
from enums import MessageEnum, UserDeleteConfirmationEnum, CommandEnum
from repository import user_repository
from languages import get_translation


async def delete_user_command(update: Update, context: CallbackContext):
    """
    유저 삭제 확인 메시지와 버튼 표시
    """
    chat_id = update.effective_chat.id
    user = user_repository.get_user(chat_id)

    if user is None:
        await update.message.reply_text(
            get_translation(MessageEnum.USER_NOT_FOUND_TO_DELETE)
        )
        return

    # 인라인 키보드 생성
    keyboard = [
        [
            InlineKeyboardButton(
                get_translation(MessageEnum.CONFIRM_YES, user.language),
                callback_data=f"{UserDeleteConfirmationEnum.CONFIRM.value}|{chat_id}",
            ),
            InlineKeyboardButton(
                get_translation(MessageEnum.CONFIRM_NO, user.language),
                callback_data=f"{UserDeleteConfirmationEnum.CANCEL.value}|{chat_id}",
            ),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # 유저에게 메시지와 키보드 보내기
    await update.message.reply_text(
        get_translation(MessageEnum.CONFIRM_DELETE_USER, user.language),
        reply_markup=reply_markup,
    )


async def handle_delete_user_callback(update: Update, context: CallbackContext):
    """
    유저 삭제 콜백 처리
    """
    query = update.callback_query

    # 콜백 데이터 분석
    data = query.data
    action, chat_id = data.split("|")

    if chat_id != str(update.effective_chat.id):
        await query.answer(
            text=get_translation(MessageEnum.INVALID_USER_ACTION), show_alert=True
        )
        return

    user = user_repository.get_user(chat_id)

    if user is None:
        await query.edit_message_text(
            text=get_translation(MessageEnum.USER_NOT_FOUND_TO_DELETE), show_alert=True
        )
        return

    user_language = user.language

    if action == UserDeleteConfirmationEnum.CONFIRM.value:
        # 유저와 관련 데이터 삭제
        user_repository.delete_user(chat_id)

        # 성공 메시지
        await query.edit_message_text(
            get_translation(MessageEnum.USER_DELETED, user_language)
        )

    elif action == UserDeleteConfirmationEnum.CANCEL.value:
        # 취소 메시지
        await query.edit_message_text(
            get_translation(MessageEnum.CANCEL_DELETE_USER, user_language)
        )


delete_user_command_handler = CommandHandler(
    CommandEnum.DELETE_USER, delete_user_command
)

# 콜백 핸들러 등록
delete_user_callback_handler = CallbackQueryHandler(
    handle_delete_user_callback,
    pattern=rf"^({UserDeleteConfirmationEnum.CONFIRM.value}|{UserDeleteConfirmationEnum.CANCEL.value})\|.*$",
)
