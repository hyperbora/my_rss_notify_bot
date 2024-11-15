import pytz
from datetime import datetime

TIMEZONE_MAP = {"en": "America/New_York", "ko": "Asia/Seoul"}


def get_user_timezone(language):
    return pytz.timezone(TIMEZONE_MAP.get(language, "UTC"))


def format_date_for_user(date: datetime, language):
    # UTC 시간대를 사용자 시간대로 변환
    utc_timezone = pytz.timezone("UTC")
    utc_time = utc_timezone.localize(date)
    user_timezone = get_user_timezone(language)
    localized_time = utc_time.astimezone(user_timezone)

    return localized_time.strftime("%Y-%m-%d %H:%M:%S")
