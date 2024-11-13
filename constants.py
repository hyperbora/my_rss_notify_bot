import os
from dotenv import load_dotenv
from enums import MessageEnum


load_dotenv()


JSON_FILE_NAME = "languages.json"
DEFAULT_LANGUAGE = MessageEnum.KO
BOT_TOKEN = os.getenv("BOT_TOKEN")
DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_TEST_URL = "sqlite:///:memory:"
MAX_RSS_FEEDS = int(os.getenv("MAX_RSS_FEEDS", "5"))
