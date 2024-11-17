import feedparser
import requests
from requests.exceptions import RequestException
from enums import MessageEnum
from utils import log_util
from constants import DEFAULT_LANGUAGE

logger = log_util.logger


def is_valid_rss(url: str) -> bool:
    """
    주어진 URL이 유효한 RSS 피드인지 확인합니다.

    Args:
        url (str): RSS 피드 URL

    Returns:
        bool: 유효한 RSS 피드라면 True, 아니면 False
    """
    try:
        # URL 요청 및 응답 확인
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생

        # 콘텐츠 강제 파싱
        feed = feedparser.parse(response.content)
    except RequestException as e:
        logger.error("Failed to fetch RSS feed: %s", url, exc_info=True)
        return False
    except Exception as e:
        logger.error(
            "Unexpected error while validating RSS feed: %s", url, exc_info=True
        )
        return False

    # feedparser의 bozo 속성이 True이면 파싱 중 오류 발생
    if feed.bozo:
        logger.warning(
            "Feed parsing error for URL: %s, Exception: %s", url, feed.bozo_exception
        )
        return False

    # 필수 필드 확인
    required_fields = ["title", "link"]
    if not all(feed.feed.get(field) for field in required_fields):
        logger.warning("Missing required fields in RSS feed: %s", url)
        return False

    return True


def get_new_rss_posts(url: str):
    """
    새로운 RSS 글을 가져오는 함수
    """
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            return feed.entries  # 새로운 RSS 글들 반환
        return []
    except Exception as e:
        logger.error("new rss posts error(%s)", url, exc_info=True)
        return []


def get_rss_feed_info(rss_url, language=DEFAULT_LANGUAGE):
    from languages import get_translation

    feed = feedparser.parse(rss_url)
    title = feed.feed.get("title", get_translation(MessageEnum.NO_TITLE, language))
    return title, rss_url


if __name__ == "__main__":
    test_url = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    print(is_valid_rss(test_url))
    print(get_new_rss_posts(test_url))
    print(get_rss_feed_info(test_url))
