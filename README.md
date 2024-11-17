# my_rss_notify_bot

RSS 새글 알림 봇

![Github URL](qr.png)

## 소개

- 사용자가 RSS 피드 주소를 등록하면 스케줄링을 특정 주기마다 실행하고 새 글이 확인되면 알림을 보내줍니다.

## 실행방법

1. 텔레그램 BotFather 토큰 발급
1. ".env_template" 파일을 복사해서 ".env" 파일로 변경
1. ".env" 파일에 BOT_TOKEN, DATABASE_FILE_NAME 및 나머지 설정 수정
1. pip install -r requirements.txt
1. python main.py

## 리눅스 서비스 등록

```sh
sudo cp my-rss-notify-bot.service /usr/lib//usr/lib/systemd/system/
cd /usr/lib/systemd/system/
sudo chown root:root my-rss-notify-bot.service
sudo chmod 644 my-rss-notify-bot.service
sudo vi my-rss-notify-bot.service
# User, Group, Environment, ExecStart등 사용환경에 맞게 수정
sudo systemctl enable my-rss-notify-bot.service
```

## 리눅스 서비스 시작 및 상태 확인

```sh
sudo systemctl start my-rss-notify-bot.service
sudo systemctl status my-rss-notify-bot.service
```

## 프로젝트 폴더 구조

```bash
├── commands/                                   # 커맨드 폴더
│   ├── __init__.py
│   ├── add_rss_command.py                      # RSS 피드 추가 커맨드
│   ├── help_command.py                         # help 커맨드
│   ├── menu_command.py                         # 봇 메뉴 등록 커맨드
│   ├── settings_command.py                     # 설정 커맨드
│   ├── show_rss_command.py                     # 등록된 RSS 피드 보여주는 커맨드
│   └── start_command.py                        # 시작 커맨드
│
├── decorators/                                 # 디코레이터 폴더
│   ├── __init__.py
│   └── user_decorators.py                      # 사용자 DB 정보 관련 디코레이터
│
├── enums/                                      # enum 정의 폴더
│   ├── __init__.py
│   ├── command_enum.py                         # 봇 커맨드 정의 enum
│   ├── message_enum.py                         # 번역 데이터 키 값 enum
│   └── user_state_enum.py                      # 커맨드에서 사용자 상태 정의하는 enum
│
├── languages/                                  # 번역 관련 폴더
│   ├── __init__.py
│   ├── languages.json                          # 번역 데이터 json
│   └── translation.py                          # json 읽어서 리턴하는 함수 정의
│
├── repository                                  # DB 관련 폴더
│   ├── __init__.py
│   ├── db.py                                   # DB 연결
│   ├── init_db.py                              # 테이블 생성
│   ├── models.py                               # SQLAlchemy 모델 정의
│   ├── rss_feed_history_repository.py          # RSS 피드 이력 관리 쿼리
│   ├── rss_feed_repository.py                  # RSS 피드 쿼리
│   └── user_repository.py                      # 유저 쿼리
│
├── tests                                       # 테스트 코드 폴더
│   ├── conftest.py                             # pytest 설정 파일
│   ├── test_01_user_repository.py              # 유저 쿼리 테스트 파일
│   ├── test_02_rss_feed_repository.py          # RSS 피드 쿼리 테스트 파일
│   └── test_03_rss_feed_history_repository.py  # RSS 피드 이력 쿼리 테스트 파일
│
├── .env                                        # 환경설정 파일
├── .env_template                               # .env 파일 생성용 템플릿 파일
├── .gitignore                                  # gitignore 파일
├── constants.py                                # .env 파일에서 읽어서 상수를 관리하는 파일
├── main.py                                     # 프로그램 시작지점
├── my-rss-notify-bot.service                   # 리눅스 서비스 파일
├── pytest.ini                                  # pytest 환경설정 파일
├── qr.png                                      # 프로젝트 QR 코드 이미지 파일
├── README.md                                   # 프로젝트 설명 파일
└── requirements.txt                            # 설치 패키지 목록
```

## 기술스택

| 라이브러리 / 도구   | 설명                                  |
| ------------------- | ------------------------------------- |
| python-telegram-bot | 파이썬 텔레그램 봇관련 패키지         |
| SQLite              | 데이터베이스                          |
| SQLAlchemy          | DB ORM                                |
| python-dotenv       | .env 파일 설정 관리                   |
| nest_asyncio        | 비동기 관련 패키지                    |
| pytest              | 테스트 도구                           |
| pytest-env          | pytest에서 env를 사용하기 위한 패키지 |
| apscheduler         | 스케줄링 패키지                       |
| feedparser          | RSS Feed parser                       |

## TODO

- 커맨드 정의

  - ~~start~~
  - ~~add_rss~~
  - ~~show_rss~~
  - ~~delete_rss~~
  - stop
  - settings
  - recent_rss

- DB 정의
  - ~~SQLAlchemy DB 스키마~~
  - ~~DB 유틸리티 py 파일~~
    - ~~User, RSS, RSS History~~
- RSS

  - ~~새 글 검색 스케줄링~~
  - ~~새 글 알림~~
  - ~~RSS 히스토리 삭제 스케줄링~~

- 기타
  - ~~다국어 처리~~
  - ~~로깅 추가~~
