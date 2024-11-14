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
RSS_CHECK_INTERVAL = int(os.getenv("RSS_CHECK_INTERVAL", "600"))
OLD_RSS_HISTORY_DAYS = int(os.getenv("OLD_RSS_HISTORY_DAYS", "30"))
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME", "rss.log")
MAX_LOG_SIZE = int(os.getenv("MAX_LOG_SIZE", "5242880"))
BACKUP_COUNT = int(os.getenv("BACKUP_COUNT", "3"))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
