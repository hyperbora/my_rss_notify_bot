from urllib.parse import urlparse
from xml.etree import ElementTree as ET
from urllib.request import urlopen
import feedparser
from enums import MessageEnum
from utils import log_util

logger = log_util.logger


def _fetch_url(url, timeout=5):
    with urlopen(url, timeout=timeout) as response:
        status_code = response.getcode()  # 상태 코드 가져오기
        content = response.read()  # 컨텐츠 가져오기
        return content, status_code


def is_valid_rss(url: str) -> bool:
    # 1. URL 형식 검사
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        return False

    # 2. RSS 피드 유효성 검사
    try:
        content, status_code = _fetch_url(url, timeout=5)
        # 상태 코드 확인 (200 OK)
        if status_code != 200:
            return False

        # XML 파싱으로 RSS 형식인지 확인
        root = ET.fromstring(content)
        if root.tag not in {"rss", "feed"}:  # rss 2.0이나 Atom 피드 여부 확인
            return False
    except Exception as e:
        logger.error("invalid rss %s", url, exc_info=True)
        return False

    return True


def get_new_rss_posts(url: str):
    """
    새로운 RSS 글을 가져오는 함수
    """
    try:
        content, _ = _fetch_url(url, timeout=10)
        feed = feedparser.parse(content)
        if feed.entries:
            return feed.entries  # 새로운 RSS 글들 반환
        return []
    except Exception as e:
        logger.error("new rss posts error(%s)", url, exc_info=True)
        return []


def get_rss_feed_info(rss_url):
    from languages import get_translation

    feed = feedparser.parse(rss_url)
    title = feed.feed.get("title", get_translation(MessageEnum.NO_TITLE))
    link = feed.feed.get("link", rss_url)
    return title, link


if __name__ == "__main__":
    test_url = "https://rss.nytimes.com/services/xml/rss/nyt/World.xml"
    print(is_valid_rss(test_url))
    print(get_new_rss_posts(test_url))
    print(get_rss_feed_info(test_url))
