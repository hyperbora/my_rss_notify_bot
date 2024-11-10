import os
from dotenv import load_dotenv
from enums import MessageEnum


load_dotenv(override=True)


JSON_FILE_NAME = "languages.json"
DEFAULT_LANGUAGE = MessageEnum.KO
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = "sqlite:///./rss.sqlite"
