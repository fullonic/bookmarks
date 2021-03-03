from types import GeneratorType

from django.db import transaction
from markers.local_observer import (
    Page,
    Watcher,
    Database,
    Bookmark,
    Subject,
    BookmarkObserver,
)
from markers.core import SimpleURL, extract_icon_from_url

FILE = "/home/somnium/.mozilla/firefox/6qsig3lq.default-1584007673559/weave/bookmarks.sqlite"
import pytest


from django.conf import settings
from markers.core import generate_tags_from_title, generate_tags_from_url, generate_tags

# ====================
# Test local observer for new bookmarks
# ====================
@pytest.mark.skip
def test_watcher_setup():
    obs = Watcher(place=FILE)
    event = obs.start()
    print(event)
    assert isinstance(obs.last_time_watch, float)

@pytest.mark.skip  # TODO: create a mark to point this local tests
def test_get_bookmarks_from_database():
    db = Database()
    items = db.get_bookmarks_items()
    urls = db.get_bookmarks_pages()
    assert isinstance(items, dict)
    assert isinstance(urls, tuple)
    assert isinstance(urls[0], Page)

@pytest.mark.skip
def test_all_bookmarks():
    from markers.local_observer import Bookmark

    db = Database()
    bookmarks = db.get_all_bookmarkers()
    assert isinstance(bookmarks, GeneratorType)
    assert isinstance(next(bookmarks), Bookmark)


@pytest.mark.xfail()
def test_get_new_records():
    """This test will fail when there is no new bookmarks.
    NOTE: Only works if a bookmark is "added by hand" before run the test.
    """
    db = Database()
    db.refresh()
    assert (1 / len(db.get_new_records())) == 1


@pytest.mark.xfail
def test_subject_emit():
    """Send data to server when emit() method is called"""
    s1 = BookmarkObserver(name="tester", url="https://www.none.net")
    Subject.attach(s1)
    db = Database()
    bookmarks = db.get_all_bookmarkers()
    data = Subject.emit([b for b in bookmarks])
    assert isinstance(data, list)
    assert isinstance(data.pop(), dict)


from markers.models import Tag, Bookmark, write_extra_info_to_table

# ====================
# Test server bookmarks service
# ====================
@pytest.mark.parametrize(
    "url",
    (
        "https://www.digikey.co.uk/en/resources/conversion-calculators/conversion-calculator-time-constant",
        "https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/",
    ),
)
def test_get_icon_from_url(url):
    icon = extract_icon_from_url(url)
    assert isinstance(icon, str)
    assert icon.startswith("http")
    assert icon.endswith(".ico")


@pytest.mark.django_db
def test_generate_favicon_on_bookmark_saving():
    new_book = Bookmark(
        url="https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/",
        title="Many-to-many relationships",
    )
    new_book.save()
    assert new_book.icon == "https://djangoproject.com/favicon.ico"


@pytest.mark.django_db
def test_add_new_bookmark_with_tags():
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


def test_generate_tags():
    title = "Visual Studio Code Tips and Tricks"
    URL = "https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/"
    tags = ["django", "python", "tips"]
    extracted_tags = generate_tags(URL, title, tags)
    assert isinstance(extracted_tags, set)
    assert "tips" in extracted_tags
    assert "django" in extracted_tags


@pytest.mark.django_db
def test_signal_create_tags(test_data, tags):
    from markers.models import Bookmark as Bookmark_model

    new_book = test_data[0].as_dict()
    book = Bookmark_model.objects.create(**new_book)
    assert "python" in book.tags.all()[0].name

@pytest.mark.skip  # TODO: How to install and run chrome on docker
@pytest.mark.django_db
def test_write_extra_info_to_table():
    url = "https://martinheinz.dev/blog/42"
    title = "Martin Heinz - Personal Website & Blog"
    book = Bookmark(url=url, title=title)
    book.save()
    write_extra_info_to_table(book.pk)
    book.refresh_from_db()
    assert book.extra_info == "Building Docker Images The Proper Way"

@pytest.mark.skip  # TODO: How to install and run chrome on docker
@pytest.mark.django_db(transaction=True)
def test_add_new_bookmark_with_extra_info():
    book = Bookmark(
        url="https://martinheinz.dev/blog/42",
        title="Martin Heinz - Personal Website & Blog",
    )
    book.save()
    book.refresh_from_db()
    assert book.extra_info == "Building Docker Images The Proper Way"

@pytest.mark.skip  # TODO: How to install and run chrome on docker
def test_uniform_schema():
    url = SimpleURL("https://martinheinz.dev/blog/42").deconstruct_url()

    assert url.scheme == "https"
    assert url.domain == "martinheinz"
    assert url.dot == "dev"
