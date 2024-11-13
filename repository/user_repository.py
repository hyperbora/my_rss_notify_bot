from typing import Optional, Generator
from repository import get_db
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


def get_all_users() -> Generator[User, None, None]:
    """
    데이터베이스에서 모든 유저를 하나씩 반환하는 제너레이터 함수.
    """
    with get_db() as db:
        query = db.query(User)
        for user in query.yield_per(10):  # 배치 크기 10으로 설정
            yield user
