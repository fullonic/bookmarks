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
import httpx

FILE = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"

# TODO: Import this from a config file
blacklist_domains = [
    "localhost",
    "fotocasa",
    "idealista",
    "wikiloc",
    "whyiexercise",
    "iwoolo",
]


@dataclass
class PageInfo:
    id: int
    title: str
    created_on: int

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
    created_on: float

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
            try:
                return json.load(f)["last_update"]
            except json.decoder.JSONDecodeError:
                pass

    @last_time_watch.setter
    def last_time_watch(self, time_):
        with open("bookmarks/config.json", "w") as f:
            json.dump({"last_update": time_}, f)

    @property
    def cursor(self):
        conn = sqlite3.connect(self.name)
        return conn.cursor()

    def _get_all_from_table(self, table):
        """Fetch bookmarks information from Firefox SQLIte database."""
        data = self.cursor.execute(f"SELECT * FROM {table};")
        return data.fetchall()

    def get_bookmarks_items(self) -> Dict[int, "PageInfo"]:
        return {
            item[10]: PageInfo(*item[8:11][::-1])
            for item in self._get_all_from_table("items")
        }

    def get_bookmarks_pages(self):
        return tuple(
            Page(id=el[0], url=el[2]) for el in self._get_all_from_table("urls")
        )

    def get_all_bookmarkers(self):
        pages = self.get_bookmarks_pages()


        items = self.get_bookmarks_items()
        bookmarks = []
        for page in pages:
            if any([domain in page.url for domain in blacklist_domains]):
                continue
            try:
                _, title, created_on = items[page.id].as_tuple()
                bookmark = Bookmark(
                    id=page.id,
                    url=page.url,
                    title=title,
                    created_on=created_on / 1000,
                )

            except KeyError:
                bookmark = Bookmark(
                    id=page.id,
                    url=page.url,
                    title=None,
                    created_on=datetime.datetime.utcnow().timestamp(),
                )

            bookmarks.append(bookmark)
            yield bookmark

    def refresh(self):
        """Get a new copy of sqlite bookmarks from firefox folder into the project folder."""
        firefox_sqlite = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"
        return shutil.copy(firefox_sqlite, self.directory)

    def get_new_records(self):
        """Get the last added bookmarks."""
        self.refresh()
        records = [
            bookmark
            for bookmark in self.get_all_bookmarkers()
            if bookmark.created_on > self.last_time_watch
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
        for sub in cls._list:
            print(f">> Sending data to {sub.name} > {sub.url}")
            for book in bookmarks:
                httpx.post(sub.url, data=book.as_dict())
        return


@dataclass
class Watcher:
    place: str
    observer = Observer()
    subscribers = Subscribers()

    def start(self):
        print(f"Observing directory: {self.place}")
        print(f"Total subscribers {len(self.subscribers.list)}")
        event_handler = Handler()
        self.observer.schedule(event_handler, self.place, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(2)
        except Exception as e:
            self.observer.stp()
            print("Error: ", e)

        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        """TODO Filter database info and send bookmarks server"""
        db = Database()
        new_records = db.get_new_records()
        if new_records:
            Subscribers.emit(new_records)


tags = "python django coding restframework restapi api testing pytest talk pycon djangocon docker docker-compose javascript golang pep medium github gitlab git repo programming programing raspberry nginx asyncio".split(
    " "
)

if __name__ == "__main__":
    # Add subscriber to event list
    myself = Subscriber(name="My Bookmarks", url="http://localhost:8000/api/bookmarks")
    Subscribers.add(myself)
    obs = Watcher(place=FILE)
    obs.start()
