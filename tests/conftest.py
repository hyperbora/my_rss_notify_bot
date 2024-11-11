import pytest
from repository import init_db


# pytest 실행 전 세팅
@pytest.fixture(scope="session", autouse=True)
def init():
    init_db()
