from enum import Enum


class DeleteActionEnum(str, Enum):
    CONFIRM_DELETE = "confirm_delete"
    CANCEL_DELETE = "cancel_delete"
