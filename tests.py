from markers.local_observer import (
    Page,
    Watcher,
    Database,
    Bookmark,
    update_server_database,
)
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

path = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave"

file = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"

import pytest


# @pytest.mark.skip
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


def test_send_formated_data():
    db = Database()
    data = db.get_all_data()
    data = update_server_database(data)
    assert len(data) > 0
    assert isinstance(data, list)
    assert isinstance(data.pop(), dict)