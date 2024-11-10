import asyncio
from telegram.ext import ApplicationBuilder
import nest_asyncio
from constants import BOT_TOKEN
from commands import get_command_handlers, set_bot_commands


async def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    for handler in get_command_handlers():
        application.add_handler(handler=handler)

    # 봇 시작 시 명령어 메뉴 설정
    await set_bot_commands(application=application)

    await application.run_polling()


if __name__ == "__main__":
    print("bot start")
    nest_asyncio.apply()
    asyncio.run(main())
