from enum import Enum


class RssFeedDeleteActionEnum(str, Enum):
    CONFIRM = "rss_feed_confirm_delete"
    CANCEL = "rss_feed_cancel_delete"
