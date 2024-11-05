import os
from dotenv import load_dotenv
from enums.message_enum import MessageEnum


load_dotenv(override=True)


JSON_FILE_NAME = "languages.json"
DEFAULT_LANGUAGE = MessageEnum.KO
BOT_TOKEN = os.getenv("BOT_TOKEN")
