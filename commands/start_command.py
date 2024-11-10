from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from enums import CommandEnum
from decorators import ensure_user_exists


@ensure_user_exists
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "안녕하세요! 아래 메뉴 버튼을 사용해 명령어를 실행할 수 있습니다."
    )


start_command_handler = CommandHandler(CommandEnum.START, start)
