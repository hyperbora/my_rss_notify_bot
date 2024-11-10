from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from enums import CommandEnum
from repository import user_repository, User
from constants import DEFAULT_LANGUAGE


async def start(update: Update, context: CallbackContext):
    user = user_repository.get_user(update.effective_chat.id)
    if user is None:
        user = User(chat_id=update.effective_chat.id, language=DEFAULT_LANGUAGE)
        user_repository.save_user(user=user)

    await update.message.reply_text(
        "안녕하세요! 아래 메뉴 버튼을 사용해 명령어를 실행할 수 있습니다."
    )


start_command_handler = CommandHandler(CommandEnum.START, start)
