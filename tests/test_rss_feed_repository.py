from repository.models import User, RSSFeed
from repository import user_repository, rss_feed_repository


def test_save_rss_feed():
    # 사용자 생성
    user = User(chat_id="12345")
    user_repository.save_user(user=user)

    # RSS 피드 생성
    rss_feed = RSSFeed(url="https://example.com/rss", user_id=user.id)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    assert saved_feed.id is not None
    assert saved_feed.url == "https://example.com/rss"
    assert saved_feed.user_id == user.id


def test_get_rss_feed():
    # RSS 피드 생성 및 저장
    rss_feed = RSSFeed(url="https://example.com/rss", user_id=1)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    # 피드 조회
    fetched_feed = rss_feed_repository.get_rss_feed(rss_feed_id=saved_feed.id)

    assert fetched_feed is not None
    assert fetched_feed.url == saved_feed.url
    assert fetched_feed.user_id == saved_feed.user_id


def test_delete_rss_feed():
    # RSS 피드 생성 및 저장
    rss_feed = RSSFeed(url="https://example.com/rss", user_id=1)
    saved_feed = rss_feed_repository.save_rss_feed(rss_feed=rss_feed)

    # 피드 삭제
    result = rss_feed_repository.delete_rss_feed(rss_feed_id=saved_feed.id)

    # 삭제된 피드 조회
    deleted_feed = rss_feed_repository.get_rss_feed(rss_feed_id=saved_feed.id)

    assert result is True
    assert deleted_feed is None


def test_get_rss_feeds_by_user_id():
    # 사용자 생성
    user = User(chat_id="67890")
    user_repository.save_user(user=user)

    # RSS 피드 2개 생성 및 저장
    rss_feed1 = RSSFeed(url="https://example.com/rss1", user_id=user.id)
    rss_feed2 = RSSFeed(url="https://example.com/rss2", user_id=user.id)
    rss_feed_repository.save_rss_feed(rss_feed=rss_feed1)
    rss_feed_repository.save_rss_feed(rss_feed=rss_feed2)

    # 사용자 ID로 RSS 피드 조회
    user_feeds = rss_feed_repository.get_rss_feeds_by_user_id(user_id=user.id)

    assert len(user_feeds) == 2
    assert user_feeds[0].url == "https://example.com/rss1"
    assert user_feeds[1].url == "https://example.com/rss2"
