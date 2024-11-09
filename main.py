import asyncio
from telegram import Update, BotCommand
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext
import nest_asyncio
from constants import BOT_TOKEN


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "안녕하세요! 아래 메뉴 버튼을 사용해 명령어를 실행할 수 있습니다."
    )


async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text(
        "도움말: 봇 사용 방법에 대한 안내를 여기에 추가하세요."
    )


async def settings(update: Update, context: CallbackContext):
    await update.message.reply_text("설정 메뉴를 여기에 추가하세요.")


async def set_menu_commands(application):
    """
    메뉴 등록
    """
    commands = [
        BotCommand(command="start", description="봇 시작"),
        BotCommand(command="help", description="도움말 보기"),
        BotCommand(command="settings", description="설정 열기"),
    ]
    await application.bot.set_my_commands(commands)


async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("settings", settings))

    # 봇 시작 시 명령어 메뉴 설정
    await set_menu_commands(application=application)

    await application.run_polling()


if __name__ == "__main__":
    print("bot start")
    nest_asyncio.apply()
    asyncio.run(main())
