import pytest
from repository.models import User
from repository.user_repository import save_user, delete_user, get_user, get_all_users


@pytest.fixture
def new_user():
    return User(chat_id="test_chat_id", language="en")


def test_get_all_users():
    users = [
        User(chat_id="user1"),
        User(chat_id="user2"),
        User(chat_id="user3"),
    ]
    for user in users:
        save_user(user=user)

    users_from_db = list(get_all_users())

    # 데이터베이스에서 가져온 유저가 sample_users와 일치하는지 확인
    assert len(users_from_db) == len(users)
    assert all(
        user.chat_id == db_user.chat_id for user, db_user in zip(users_from_db, users)
    )


def test_save_user(new_user):
    saved_user = save_user(new_user)
    assert saved_user.id is not None
    assert saved_user.chat_id == "test_chat_id"
    assert saved_user.language == "en"


def test_get_user(new_user):
    user = get_user(chat_id="test_chat_id")
    assert user is not None
    assert user.chat_id == "test_chat_id"
    assert user.language == "en"


def test_delete_user(new_user):
    result = delete_user(chat_id="test_chat_id")
    assert result is True
    user = get_user(chat_id="test_chat_id")
    assert user is None
