import os
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from constants import DATABASE_URL, DATABASE_TEST_URL

URL = DATABASE_URL
if os.environ.get("ENVIRONMENT") == "TEST":
    URL = DATABASE_TEST_URL

# SQLAlchemy 설정
engine = create_engine(URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 모델을 위한 기본 클래스
Base = declarative_base()


# 데이터베이스 세션을 가져오는 함수
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
