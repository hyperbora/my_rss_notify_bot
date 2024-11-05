import json
import os
from constants import DEFAULT_LANGUAGE, JSON_FILE_NAME


def load_translations():
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(cur_dir, JSON_FILE_NAME), "r", encoding="utf-8") as file:
        return json.load(file)


TRANSLATIONS = load_translations()


def get_translation(key, language=DEFAULT_LANGUAGE):
    return TRANSLATIONS.get(language, DEFAULT_LANGUAGE).get(key, key)
