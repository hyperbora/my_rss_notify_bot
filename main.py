import os
from telegram.ext import ApplicationBuilder
from dotenv import load_dotenv

load_dotenv(override=True)


def main():
    BOT_TOKN = os.getenv("BOT_TOKEN")
    application = ApplicationBuilder().token(BOT_TOKN).build()

    application.run_polling()


if __name__ == "__main__":
    print("bot start")
    main()
