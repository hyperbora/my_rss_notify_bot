from telegram.ext import Application
from .start_command import start_command_handler
from .help_command import help_command_handler
from .settings_command import settings_command_handler
from .menu_command import menu_commands
from .add_rss_command import add_rss_handler
from .show_rss_command import show_rss_command_handler
from .delete_rss_command import (
    delete_rss_command_handler,
    confirm_delete_rss_callback_query_handler,
    handle_confirm_delete_callback_query_handler,
)

__all__ = [
    "start_command_handler",
    "help_command_handler",
    "settings_command_handler",
    "add_rss_handler",
    "show_rss_command_handler",
    "delete_rss_command_handler",
    "confirm_delete_rss_callback_query_handler",
    "handle_confirm_delete_callback_query_handler",
]


def get_command_handlers():
    return [
        start_command_handler,
        help_command_handler,
        settings_command_handler,
        add_rss_handler,
        show_rss_command_handler,
        delete_rss_command_handler,
        confirm_delete_rss_callback_query_handler,
        handle_confirm_delete_callback_query_handler,
    ]


def set_bot_commands(application: Application):
    return application.bot.set_my_commands(menu_commands)
