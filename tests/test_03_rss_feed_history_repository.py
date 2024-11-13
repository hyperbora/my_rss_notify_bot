import pytest
from datetime import datetime
from repository.models import User, RSSFeed, RSSFeedHistory
from repository import user_repository, rss_feed_repository, rss_feed_history_repository


@pytest.fixture(scope="function")
def user():
    # 테스트용 유저 생성
    chat_id = "12345"
    found_user = user_repository.get_user(chat_id=chat_id)
    if found_user is None:
        found_user = user_repository.save_user(user=User(chat_id=chat_id))
    return found_user


@pytest.fixture(scope="function")
def rss_feed(user):
    # 테스트용 RSS 피드 생성
    rss_feed = RSSFeed(url="http://example.com/rss", user_id=user.id)
    rss_feed_repository.save_rss_feed(rss_feed)
    return rss_feed


@pytest.fixture(scope="function")
def rss_feed_history(rss_feed):
    # 테스트용 RSS 피드 히스토리 생성
    history = RSSFeedHistory(
        rss_feed_id=rss_feed.id,
        entry_id="unique_entry_id",
        title="Example Entry",
        link="http://example.com/rss/entry",
        published_at=datetime.now(),
    )
    rss_feed_history_repository.save_entry(history)
    return history


def test_save_rss_feed_history(rss_feed):
    # 새 RSS 피드 히스토리 항목 저장
    history = RSSFeedHistory(
        rss_feed_id=rss_feed.id,
        entry_id="another_unique_entry_id",
        title="New Entry",
        link="http://example.com/rss/new-entry",
        published_at=datetime.now(),
    )
    saved_history = rss_feed_history_repository.save_entry(history)

    assert saved_history.id is not None
    assert saved_history.entry_id == "another_unique_entry_id"
    assert saved_history.title == "New Entry"
    assert saved_history.link == "http://example.com/rss/new-entry"
    assert saved_history.rss_feed_id == rss_feed.id


def test_get_rss_feed_history_by_entry_id(rss_feed_history):
    # entry_id로 RSS 피드 히스토리 조회
    history = rss_feed_history_repository.get_entry_by_feed_and_entry_id(
        rss_feed_id=rss_feed_history.rss_feed_id, entry_id=rss_feed_history.entry_id
    )

    assert history is not None
    assert history.entry_id == rss_feed_history.entry_id
    assert history.title == rss_feed_history.title
    assert history.link == rss_feed_history.link
    assert history.published_at == rss_feed_history.published_at
    assert history.rss_feed_id == rss_feed_history.rss_feed_id
