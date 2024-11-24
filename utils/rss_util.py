import feedparser
from feedparser import NonXMLContentType
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
    feed = feedparser.parse(url)
    # 'bozo'가 0이면 RSS 파싱에 문제가 없음을 의미
    if feed.bozo == 1:
        if isinstance(feed.bozo_exception, NonXMLContentType):
            logger.warning("Warning: Non-XML media type. Ignoring this error.")
        else:
            logger.error("Error parsing RSS feed: %s", feed.bozo_exception)
            return False
    # 'feed' 딕셔너리에 'title'이나 기타 주요 정보가 있어야 유효한 피드
    if not feed.feed.get("title"):
        logger.error("Invalid RSS feed: Missing title or feed metadata.")
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
