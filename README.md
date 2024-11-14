# my_rss_notify_bot

RSS 새글 알림 봇

![Github URL](qr.png)

## 소개

- 사용자가 RSS 피드 주소를 등록하면 스케줄링을 특정 주기마다 실행하고 새 글이 확인되면 알림을 보내줍니다.

## 실행방법

1. 텔레그램 BotFather 토큰 발급
1. ".env_template" 파일을 복사해서 ".env" 파일로 변경
1. ".env" 파일에 BOT_TOKEN, DATABASE_FILE_NAME 및 나머지 설정 수정
1. pip install -r
1. python main.py

## 리눅스 서비스 등록

```sh
sudo cp my-rss-notify-bot.service /usr/lib//usr/lib/systemd/system/
cd /usr/lib//usr/lib/systemd/system/
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

## 기술스택

- python-telegram-bot
  - 파이썬 텔레그램 봇관련 패키지
- SQLAlchemy
  - DB ORM
- python-dotenv
  - .env 파일 설정 관리
- nest_asyncio
  - 비동기 관련 패키지
- pytest
  - 테스트 도구
- pytest-env
  - pytest에서 env를 사용하기 위한 패키지
- apscheduler
  - 스케줄링 패키지
- feedparser
  - RSS Feed parser

## TODO

- 커맨드 정의

  - ~~start~~
  - ~~add_rss~~
  - show_rss
  - delete_rss
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
