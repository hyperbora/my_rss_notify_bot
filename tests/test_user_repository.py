import pytest
from repository.models import User
from repository.user_repository import save_user, delete_user, get_user


@pytest.fixture
def new_user():
    return User(chat_id="test_chat_id", language="en")


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
