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
    PROMPT_ENTER_RSS_URL = "prompt_enter_rss_url"
    SUCCESS_RSS_ADDED = "success_rss_added"
    ERROR_RSS_ADD_FAILED = "error_rss_add_failed"
    CANCEL_RSS_ADD = "cancel_rss_add"
    RSS_ALREADY_EXISTS = "rss_already_exists"
    RSS_MAX_LIMIT = "rss_max_limit"
    INVALID_RSS_URL = "invalid_rss_url"
    NEW_RSS_UPDATES = "new_rss_updates"
    SOURCE = "source"
    MORE_UPDATES = "more_updates"
    CLICK_TO_VIEW = "click_to_view"
    NO_TITLE = "no_title"
    NO_RSS_FEEDS_REGISTERED = "no_rss_feeds_registered"
    ERROR_FETCHING_RSS_FEEDS = "error_fetching_rss_feeds"
    REGISTERED_RSS_FEED_LIST = "registered_rss_feed_list"
    NO_UPDATE_INFORMATION = "no_update_information"
    LAST_UPDATED = "last_updated"
    NO_RSS_TO_DELETE = "no_rss_to_delete"
    SELECT_RSS_TO_DELETE = "select_rss_to_delete"
    CONFIRM_YES = "confirm_yes"
    CONFIRM_NO = "confirm_no"
    CONFIRM_DELETE_RSS = "confirm_delete_rss"
    RSS_DELETED_SUCCESS = "rss_deleted_success"
    RSS_DELETED_CONFIRM = "rss_deleted_confirm"
    DELETE_CANCELED = "delete_canceled"
    DELETE_OPERATION_CANCELED = "delete_operation_canceled"
    USER_NOT_FOUND_TO_DELETE = "user_not_found"
    CONFIRM_DELETE_USER = "confirm_delete_user"
    INVALID_USER_ACTION = "invalid_user_action"
    USER_DELETED = "user_deleted"
    CANCEL_DELETE_USER = "cancel_delete_user"
    PREPARING = "preparing"
