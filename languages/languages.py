import json
import os
from constants import DEFAULT_LANGUAGE, JSON_FILE_NAME


def load_translations():
    """
    Load translations from a JSON file.

    Reads the translation data from a JSON file located in the current directory.
    If the file is not found or contains invalid JSON, an empty dictionary is returned.

    Returns:
        dict: A dictionary containing translations for each language.
    """
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    try:
        with open(os.path.join(cur_dir, JSON_FILE_NAME), "r", encoding="utf-8") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading translations: {e}")
        return {}


_translations = load_translations()


def get_translation(key, language=DEFAULT_LANGUAGE):
    """
    Retrieve a translation for a specific key and language.

    Fetches the translation for the given key in the specified language.
    If the key is not found in the specified language, it falls back to the default language.
    If the key is still not found, the key itself is returned as a fallback.

    Args:
        key (str): The key for the desired translation.
        language (str): The language code (default is the default language).

    Returns:
        str: The translated text, or the key itself if no translation is found.
    """
    translation = _translations.get(language, {})
    return translation.get(key, _translations[DEFAULT_LANGUAGE].get(key, key))


def reload_translations():
    """
    Reload the translation data from the JSON file.

    Re-reads the JSON file to refresh translation data. This function is useful
    when the JSON file is updated and needs to reflect changes in the application.

    Side Effects:
        Updates the `_translations` global variable with the latest translations.
    """
    global _translations
    _translations = load_translations()
