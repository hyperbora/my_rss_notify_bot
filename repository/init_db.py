from .db import engine, Base
from .models import User, RSSFeed


# 데이터베이스에 테이블 생성
def init_db():
    Base.metadata.create_all(bind=engine)
