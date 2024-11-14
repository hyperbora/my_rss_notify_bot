import logging
import sys
from logging.handlers import RotatingFileHandler
from constants import LOG_FILE_PATH, MAX_LOG_SIZE, BACKUP_COUNT, LOG_LEVEL


class StreamToLogger(object):
    """
    Fake file-like stream object that redirects writes to a logger instance.
    """

    def __init__(self, st_logger, st_level):
        self.logger = st_logger
        self.level = st_level
        self.linebuf = ""

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass


level = getattr(logging, LOG_LEVEL)

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

sys.stdout = StreamToLogger(logger, logging.INFO)
sys.stderr = StreamToLogger(logger, logging.ERROR)
