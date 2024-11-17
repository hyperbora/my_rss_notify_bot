from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from enums import CommandEnum, MessageEnum
from languages import get_translation
from decorators import ensure_user_exists
from repository import User


@ensure_user_exists
async def settings(update: Update, context: CallbackContext, user: User):
    await update.message.reply_text(
        get_translation(MessageEnum.PREPARING, user.language)
    )


settings_command_handler = CommandHandler(CommandEnum.SETTINGS, settings)
