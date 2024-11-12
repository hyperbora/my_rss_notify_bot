from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from enums import CommandEnum, MessageEnum
from languages import get_translation


async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(get_translation(MessageEnum.HELP_MESSAGE))


help_command_handler = CommandHandler(CommandEnum.HELP, help_command)
