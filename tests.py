import time

from markers.local_observer import Watcher
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

path = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave"

file = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"


def test_watcher_setup():
    obs = Watcher()
    assert isinstance(obs.last_time_watch, float)


def test_observer():
    w = Watcher()
    w.place = file
    w.start()