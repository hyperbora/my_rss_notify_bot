from enum import Enum


class MessageEnum(str, Enum):
    KO = "ko"
    EN = "en"
    WELCOME_MESSAGE = "welcome_message"
    HELP_MESSAGE = "help_message"
    RSS_ADDED = "rss_added"
    RSS_REMOVED = "rss_removed"
    NO_RSS_FEEDS = "no_rss_feeds"
    WAITING_FOR_RSS = "waiting_for_rss"
    WAITING_FOR_REMOVE_RSS = "waiting_for_remove_rss"
    START = "start"
    HELP = "help"
    ADD_RSS = "add_rss"
    REMOVE_RSS = "remove_rss"
    SHOW_RSS = "show_rss"
    STOP = "stop"
    ADD_RSS_MESSAGE_KEY = "add_rss_message_key"
    STOP_MESSAGE = "stop_message"
