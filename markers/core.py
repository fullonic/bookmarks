from pathlib import Path

from .models import Items, Tags

import datetime
from dataclasses import dataclass, field

import json


def get_config():
    with open("bookmarks/config.json") as f:
        return json.load(f)
    # return cfg


def update_config(key, value):
    cfg = get_config()
    # update
    cfg[key] = value
    with open("bookmarks/config.json", "w") as f:
        json.dump(cfg, f)


def last_time_updated():
    cfg = get_config()
    return cfg["last_update"]


import shutil


def check_for_new_bookmarks_update():
    """Check if there is any new bookmark and if exist, update current db version."""
    db_file = "bookmarks.sqlite"
    db_original_path = Path(
        f"/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/{db_file}"
    )
    last_modification = db_original_path.stat().st_mtime
    last_time_checked = last_time_updated()
    if last_modification > last_time_checked:
        print(">> New updated will be performed")
        project_folder = Path(__file__).resolve().parent.parent
        shutil.copy(db_original_path, project_folder)
        return update_tags_table()
    print(">> Database up to date.")
    # return


@dataclass
class Bookmark:
    pk: int
    url: str
    title: str
    description: str
    add_at: datetime.datetime
    tags: set = field(default_factory=set)


# Useful tags
tags = {
    "backup",
    "celery",
    "code",
    "redis",
    "compose",
    "db",
    "django",
    "docker",
    "docker-compose",
    "drf",
    "http headers",
    "permissions",
    "postgres",
    "rest",
    "restful",
    "api",
    "python",
    "python library",
    "python stdlib",
    "security",
    "translate",
    "web",
    "task queues",
    "queues",
    "tips",
    "best practices",
    "djangocon",
    "pycon",
    "github",
    "design patterns",
    "testing",
    "pytest",
    "nginx",
}


def clean_database():
    # Remove non coding url based on tags
    print(">> Removing non code tags and corespondent urls")
    for el in Tags.objects.all():
        if el.tag not in tags:
            el.delete()


def generate_tag_url(url):
    return [tag for tag in tags if tag in url]


def generate_tag_title(title):
    return [tag for tag in tags if tag in title.lower()]


def filtered_database_records():
    # get list of filtered data
    print(">> Filtering and merging items and urls information.")
    return (
        Bookmark(
            el.pk,
            el.urlid.url,
            el.title,
            el.description,
            datetime.datetime.fromtimestamp(el.dateadded / 1000),
            tags=set([*generate_tag_url(el.urlid.url), *generate_tag_title(el.title)]),
        )
        for el in Items.objects.select_related("urlid").all()
        if el.urlid is not None and ((el.dateadded / 1000) > last_time_updated())
    )


def update_tags_table():
    clean_database()
    print(">> Add tags with items to Tag table.")
    for idx, item in enumerate(filtered_database_records()):
        bookmark = Items.objects.get(pk=item.pk)
        for tag in item.tags:
            Tags.objects.get_or_create(tag=tag, itemid=bookmark)
    update_config("last_update", datetime.datetime.now().timestamp())


import sqlite3


def db_cursor():
    db = Path(__file__).resolve().parent.parent / "bookmarks.sqlite"
    conn = sqlite3.connect(db)
    return conn.cursor()
    # conn.close()
    # print("Connection closed!")


@dataclass
class UrlMeta:
    id: int
    title: str
    add_date_on: int


def get_item_from_db():
    c = db_cursor()
    items = c.execute("select * from items;")
    return items.fetchall()


def read_items():
    url_list = [UrlMeta(*item[8:11]) for item in get_item_from_db()]
    print(">> Done!")
    print(len(url_list))
