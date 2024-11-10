from telegram.ext import Application
from .start_command import start_command_handler
from .help_command import help_command_handler
from .settings_command import settings_command_handler
from .menu_command import menu_commands

__all__ = ["start_command_handler", "help_command_handler", "settings_command_handler"]


def get_command_handlers():
    return [start_command_handler, help_command_handler, settings_command_handler]


def set_bot_commands(application: Application):
    return application.bot.set_my_commands(menu_commands)
