import logging
import sys
from logging.handlers import RotatingFileHandler
from constants import LOG_FILE_PATH, MAX_LOG_SIZE, BACKUP_COUNT, LOG_LEVEL

level = logging.getLevelNamesMapping().get(LOG_LEVEL, logging.INFO)

# 로거 초기화
logger = logging.getLogger(__file__)
logger.setLevel(level)

# 로그 포맷 설정
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] %(filename)s: %(message)s", "%Y-%m-%d %H:%M:%S"
)

# 파일 핸들러 설정 (회전 파일 핸들러)
file_handler = RotatingFileHandler(
    LOG_FILE_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT
)
file_handler.setFormatter(formatter)
file_handler.setLevel(level)

# 로거에 파일 핸들러 추가
logger.addHandler(file_handler)

# stderr 로그도 파일에 기록
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setFormatter(formatter)
stderr_handler.setLevel(logging.ERROR)
logger.addHandler(stderr_handler)
