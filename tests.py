from markers.local_observer import (
    Page,
    Watcher,
    Database,
    Bookmark,
    Subscribers,
    Subscriber,
)


FILE = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"
import os
import pytest

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmarks.settings")
from django.conf import settings
from markers.core import generate_tags_from_title, generate_tags_from_url

# settings.configure()


@pytest.mark.skip
def test_watcher_setup():
    obs = Watcher()
    obs.place = FILE
    event = obs.start()
    print(event)
    assert isinstance(obs.last_time_watch, float)


def test_get_bookmarks_from_database():
    db = Database()
    items = db.get_bookmarks_items()
    urls = db.get_bookmarks_urls()
    assert isinstance(items, dict)
    assert isinstance(urls, tuple)
    assert isinstance(urls[0], Page)


def test_all_bookmarks():
    db = Database()
    bookmarks = db.get_all_data()
    assert isinstance(bookmarks, list)
    assert isinstance(bookmarks[0], Bookmark)


@pytest.mark.xfail()
def test_get_new_records():
    """This test will fail when there is no new bookmarks.
    NOTE: Only works if a bookmark is "added by hand" before run the test.
    """
    db = Database()
    db.refresh()
    assert (1 / len(db.get_new_records())) == 1


def test_subscribers_emit():
    """Send data to server when emit() method is called"""
    s1 = Subscriber(name="tester", url="www.none.net")
    s2 = Subscriber(name="tester2", url="www.none.net")
    Subscribers.add(s1)
    Subscribers.add(s2)
    db = Database()
    bookmarks = db.get_all_data()
    data = Subscribers.emit(bookmarks)
    assert isinstance(data, list)
    assert isinstance(data.pop(), dict)


@pytest.mark.django_db
def test_add_new_bookmark_with_tags():
    from markers.models import Tag, Bookmark

    TAG = "django"
    URL = "https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/"
    Tag.objects.get_or_create(name=TAG)
    marker = Bookmark.objects.create(
        url=URL,
        title="Many-to-many relationships",
    )

    tag = Tag.objects.get(pk=1)
    marker.tags.add(tag)
    assert len(marker.tags.all()) == 1
    assert marker.tags.first().name == TAG
    # check reverse access
    assert tag.bookmark_set.first().url == URL


def test_extract_tags_from_url():
    URL = "https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/"
    tags = ["django", "python", "docs"]
    extracted_tags = generate_tags_from_url(URL, tags)
    assert "django" in extracted_tags
    assert "docs" in extracted_tags
    assert "python" not in extracted_tags


def test_extract_tags_from_title():
    title = "Visual Studio Code Tips and Tricks"
    tags = ["django", "tips"]
    extracted_tags = generate_tags_from_title(title, tags)
    assert "tips" in extracted_tags
    assert "django" not in extracted_tags
