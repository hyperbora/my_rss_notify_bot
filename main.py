from telegram.ext import ApplicationBuilder
from constants import BOT_TOKEN


def main():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.run_polling()


if __name__ == "__main__":
    print("bot start")
    main()
