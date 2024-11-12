from enum import Enum


class CommandEnum(str, Enum):
    START = "start"
    HELP = "help"
    SETTINGS = "settings"
    ADD_RSS = "add_rss"
    CANCEL_RSS_ADD = "cancel_rss_add"
