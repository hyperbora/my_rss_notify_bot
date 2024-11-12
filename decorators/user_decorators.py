from functools import wraps
from telegram import Update
from repository import user_repository, User
from constants import DEFAULT_LANGUAGE


def ensure_user_exists(func):
    @wraps(func)
    async def wrapper(update: Update, context, *args, **kwargs):
        user = user_repository.get_user(update.effective_chat.id)
        if user is None:
            # 유저가 없으면 기본값을 설정하여 새로 생성
            user = User(chat_id=update.effective_chat.id, language=DEFAULT_LANGUAGE)
            user_repository.save_user(user)
        return await func(update, context, user, *args, **kwargs)  # 원래의 함수 호출

    return wrapper
