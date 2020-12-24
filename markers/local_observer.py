from pathlib import Path
import sqlite3
from dataclasses import dataclass
import time
from watchdog import observers
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
import json


@dataclass
class PageInfo:
    id: int
    title: str
    add_date_on: int


@dataclass
class Page:
    url: str


class Watcher:
    place: str
    observer = Observer()

    @property
    def last_time_watch(self):
        with open("bookmarks/config.json") as f:
            return json.load(f)["last_update"]

    def start(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.place, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print("Error: ", e)

        finally:
            self.observer.join()


class Handler(FileSystemEventHandler):
    @staticmethod
    def on_modified(event):
        """TODO Filter database info and send to bookmarks server"""
        print(f"Received modified event -  {event.src_path}")


def db_cursor():
    db = Path(__file__).resolve().parent.parent / "bookmarks.sqlite"
    conn = sqlite3.connect(db)
    return conn.cursor()


def get_item_from_db():
    c = db_cursor()
    items = c.execute("select * from items;")
    return items.fetchall()


def read_items():
    url_list = [PageInfo(*item[8:11]) for item in get_item_from_db()]
    print(">> Done!")
    print(len(url_list))
