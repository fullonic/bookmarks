import datetime
from pathlib import Path
import sqlite3
from dataclasses import dataclass, astuple, asdict
import time
from typing import Dict
from watchdog import observers
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import json
import shutil

FILE = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"


@dataclass
class PageInfo:
    id: int
    title: str
    add_date_on: int

    def as_tuple(self):
        return astuple(self)


@dataclass
class Page:
    id: int
    url: str


@dataclass
class Bookmark:
    id: int
    url: str
    title: str
    add_date_on: float

    def as_dict(self):
        return asdict(self)


class Database:
    directory = Path(__file__).resolve().parent.parent

    @property
    def name(self):
        return self.directory / "bookmarks.sqlite"

    @property
    def last_time_watch(self):
        with open("bookmarks/config.json") as f:
            return json.load(f)["last_update"]

    @last_time_watch.setter
    def last_time_watch(self, time_):
        with open("bookmarks/config.json", "w") as f:
            json.dump({"last_update": time_}, f)

    @property
    def cursor(self):
        conn = sqlite3.connect(self.name)
        return conn.cursor()

    def _get_all_from_table(self, table):
        data = self.cursor.execute(f"SELECT * FROM {table};")
        return data.fetchall()

    def get_bookmarks_items(self) -> Dict[int, "PageInfo"]:
        return {
            item[10]: PageInfo(*item[8:11][::-1])
            for item in self._get_all_from_table("items")
        }

    def get_bookmarks_urls(self):
        return tuple(
            Page(id=el[0], url=el[2]) for el in self._get_all_from_table("urls")
        )

    def get_all_data(self):
        urls = self.get_bookmarks_urls()
        items = self.get_bookmarks_items()
        bookmarks = []
        for url in urls:
            try:
                _, title, add_date_on = items[url.id].as_tuple()
                bookmark = Bookmark(
                    id=url.id,
                    url=url.url,
                    title=title,
                    add_date_on=add_date_on / 1000,
                )

            except KeyError:
                bookmark = Bookmark(
                    id=url.id,
                    url=url.url,
                    title=None,
                    add_date_on=0,
                )
            finally:
                bookmarks.append(bookmark)
        return bookmarks

    def refresh(self):
        """Get a new copy of sqlite bookmarks from firefox folder into the project folder."""
        firefox_sqlite = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"
        return shutil.copy(firefox_sqlite, self.directory)

    def get_new_records(self):
        """Get the last added bookmarks."""
        self.refresh()
        records = [
            bookmark
            for bookmark in self.get_all_data()
            if bookmark.add_date_on > self.last_time_watch
        ]

        self.last_time_watch = datetime.datetime.now().timestamp()
        return records


@dataclass(eq=True, frozen=True)
class Subscriber:
    """Add equality"""

    name: str
    url: str


class Subscribers:
    _list = []

    @property
    def list(cls):
        return cls._list

    @classmethod
    def add(cls, subscriber):
        cls._list.append(subscriber)

    @classmethod
    def emit(cls, bookmarks):
        print(">> Sending data to server")
        data = [book.as_dict() for book in bookmarks]
        for sub in cls.list:
            # post data to server with httpx.post()
            print(sub)
        return data


class Watcher:
    place: str = FILE
    observer = Observer()
    subscribers = Subscribers()

    def start(self):
        event_handler = Handler(self.subscribers)
        self.observer.schedule(event_handler, self.place, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(10)
        except Exception as e:
            self.observer.stp()
            print("Error: ", e)

        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        """TODO Filter database info and send to bookmarks server"""
        db = Database()
        new_records = db.get_new_records()
        # if new_records:
        #     update_server_database(new_records)
