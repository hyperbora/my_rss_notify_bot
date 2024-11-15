import pytz

TIMEZONE_MAP = {"en": "America/New_York", "ko": "Asia/Seoul"}


def get_user_timezone(language):
    return pytz.timezone(TIMEZONE_MAP.get(language, "UTC"))


def format_date_for_user(date, language):
    # UTC 시간대를 사용자 시간대로 변환
    user_timezone = get_user_timezone(language)
    return date.astimezone(user_timezone).strftime("%Y-%m-%d %H:%M:%S")
