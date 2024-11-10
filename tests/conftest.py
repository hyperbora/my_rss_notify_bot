import os
import pytest


# pytest 실행 전 테스트 환경 변수 설정
@pytest.fixture(scope="session", autouse=True)
def set_environment():
    # TEST 환경으로 설정
    os.environ["ENVIRONMENT"] = "TEST"
