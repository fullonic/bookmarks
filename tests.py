from markers.local_observer import (
    Page,
    Watcher,
    Database,
    Bookmark,
    # update_server_database,
    Subscribers,
    Subscriber,
)
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

path = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave"

file = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"

import pytest


@pytest.mark.skip
def test_watcher_setup():
    obs = Watcher()
    obs.place = file
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
