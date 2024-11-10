from typing import Optional
from repository.db import get_db
from repository.models import User


def save_user(user: User) -> User:
    try:
        with get_db() as db:
            db.add(user)
            db.commit()
            db.refresh(user)
            return user
    except Exception as e:
        db.rollback()
        raise e


def get_user(chat_id: str) -> Optional[User]:
    with get_db() as db:
        return db.query(User).filter(User.chat_id == chat_id).first()


def delete_user(chat_id: str) -> bool:
    try:
        with get_db() as db:
            user = get_user(chat_id=chat_id)
            if user:
                db.delete(user)
                db.commit()
                return True
            return False
    except Exception as e:
        db.rollback()
        raise e
