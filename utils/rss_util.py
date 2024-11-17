import feedparser
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
        feed = feedparser.parse(url)
        # feedparser의 bozo 속성이 True이면 파싱 중 오류가 발생했음을 의미합니다.
        if feed.bozo:
            return False

        # 채널의 필수 속성 중 하나라도 없다면 유효하지 않은 RSS로 간주
        required_fields = ["title", "link", "description"]
        return all(getattr(feed.feed, field, None) for field in required_fields)
    except Exception as e:
        logger.error("Error validating RSS feed: {%s}", url, exc_info=True)
        return False


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
