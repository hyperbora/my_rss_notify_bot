from telegram import BotCommand
from enums import CommandEnum

# 메뉴에 표시할 명령어와 설명을 정의
menu_commands = [
    BotCommand(CommandEnum.START, "봇 시작"),
    BotCommand(CommandEnum.ADD_RSS, "RSS 추가"),
    BotCommand(CommandEnum.SHOW_RSS, "등록된 RSS 목록"),
    BotCommand(CommandEnum.DELETE_RSS, "RSS 삭제"),
    BotCommand(CommandEnum.HELP, "도움말 보기"),
    BotCommand(CommandEnum.SETTINGS, "설정 열기"),
]
