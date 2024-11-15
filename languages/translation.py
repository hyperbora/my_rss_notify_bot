import json
import os
from constants import DEFAULT_LANGUAGE, JSON_FILE_NAME
from enums import MessageEnum
from utils import log_util

logger = log_util.logger


def load_translations():
    """
    JSON 파일에서 번역 데이터 읽기
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(os.path.join(cur_dir, JSON_FILE_NAME), "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error("Error loading translations", exc_info=True)
        return {}


_translations = load_translations()


def get_translation(key: MessageEnum, language=DEFAULT_LANGUAGE, **kwargs):
    """
    키값, 언어, 파라미터 있어서 지정하면 번역 문장 리턴
    """
    translation = _translations.get(language, {})
    message = translation.get(key, _translations[DEFAULT_LANGUAGE].get(key, key))
    return message.format(**kwargs) if kwargs else message


def reload_translations():
    """
    번역 데이터 재적용
    """
    global _translations
    _translations = load_translations()
