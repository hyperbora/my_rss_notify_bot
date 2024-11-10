from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from enums import CommandEnum


async def settings(update: Update, context: CallbackContext):
    await update.message.reply_text("설정 메뉴를 여기에 추가하세요.")


settings_command_handler = CommandHandler(CommandEnum.SETTINGS, settings)
