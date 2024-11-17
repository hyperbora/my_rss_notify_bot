from enum import Enum


class UserDeleteConfirmationEnum(str, Enum):
    CONFIRM = "user_confirm_delete"
    CANCEL = "user_cancel_delete"
