from telegram import Update
from telegram.ext import CommandHandler, CallbackContext


async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "도움말: 봇 사용 방법에 대한 안내를 여기에 추가하세요."
    )


help_command_handler = CommandHandler("help", help_command)
