import pytest
from repository.models import User, RSSFeed
from repository import user_repository, rss_feed_repository


@pytest.fixture(scope="function")
def user():
    """
    테스트용 유저 생성
    """

    chat_id = "12345"
    found_user = user_repository.get_user(chat_id=chat_id)
    if found_user is None:
        found_user = user_repository.save_user(user=User(chat_id=chat_id))
    return found_user


def test_get_rss_feed_count_by_user_id(user):
    """
    피드 count 함수 테스트
    """

    for i in range(3):
        rss_feed = RSSFeed(url=f"http://rssfeed{i}.com", user_id=user.id)
        rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    count = rss_feed_repository.get_rss_feed_count_by_user_id(user.id)
    assert count == 3


def test_save_rss_feed(user):
    """
    RSS 피드 저장 테스트
    """

    rss_feed = RSSFeed(url="https://example.com/rss", user_id=user.id)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    assert saved_feed.id is not None
    assert saved_feed.url == "https://example.com/rss"
    assert saved_feed.user_id == user.id


def test_get_rss_feed(user):
    """
    RSS 피드 조회 테스트
    """

    rss_feed = RSSFeed(url="https://example.com/rss", user_id=user.id)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    fetched_feed = rss_feed_repository.get_rss_feed(rss_feed_id=saved_feed.id)

    assert fetched_feed is not None
    assert fetched_feed.url == saved_feed.url
    assert fetched_feed.user_id == saved_feed.user_id


def test_delete_rss_feed(user):
    """
    RSS 피드 삭제 테스트
    """

    rss_feed = RSSFeed(url="https://example.com/rss", user_id=user.id)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    result = rss_feed_repository.delete_rss_feed(rss_feed_id=saved_feed.id)

    deleted_feed = rss_feed_repository.get_rss_feed(rss_feed_id=saved_feed.id)

    assert result is True
    assert deleted_feed is None


def test_get_rss_feeds_by_user_id():
    """
    RSS 피드 리스트 조회
    """

    new_user = User(chat_id="67890")
    user_repository.save_user(user=new_user)

    rss_feed1 = RSSFeed(url="https://example.com/rss1", user_id=new_user.id)
    rss_feed2 = RSSFeed(url="https://example.com/rss2", user_id=new_user.id)
    rss_feed_repository.save_rss_feed(rss_feed=rss_feed1)
    rss_feed_repository.save_rss_feed(rss_feed=rss_feed2)

    user_feeds = rss_feed_repository.get_rss_feeds_by_user_id(user_id=new_user.id)

    assert len(user_feeds) == 2
    assert user_feeds[0].url == "https://example.com/rss1"
    assert user_feeds[1].url == "https://example.com/rss2"
