from enum import Enum


class CommandEnum(str, Enum):
    START = "start"
    HELP = "help"
    SETTINGS = "settings"
