import os
import pytest
from django.conf import settings  # noqa


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmarks.settings")
from rest_framework.test import APIClient
from markers.local_observer import Bookmark
from django.contrib.auth import get_user_model


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """

    ...


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture
def api_client_authenticate(db, api_client):
    user = get_user_model().objects.create(username="auth", password="password")
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture()
def test_data():
    return [
        Bookmark(
            id=101,
            url="https://www.youtube.com/watch?v=qkGxy4c64Jg",
            title="Import as an antipattern - Demystifying Dependency Injection in modern Python - YouTube",
            created_on=1588246982.166,
        ),
        Bookmark(
            id=102,
            url="https://towardsdatascience.com/build-a-custom-trained-object-detection-model-with-5-lines-of-code-713ba7f6c0fb",
            title="Build a custom-trained object detection model with 5 lines of code",
            created_on=1583185176.479,
        ),
        Bookmark(
            id=103,
            url="https://www.flaticon.com/free-icon/eel_1625250?term=eel&page=1&position=23",
            title="Eel Icons - 72 free vector icons",
            created_on=1579844103.249,
        ),
        Bookmark(
            id=104,
            url="https://medium.com/coding-blocks/creating-user-database-and-adding-access-on-postgresql-8bfcd2f4a91e",
            title="Creating user, database and adding access on PostgreSQL",
            created_on=1557157558.913,
        ),
        Bookmark(
            id=105,
            url="https://www.youtube.com/watch?v=_jQ3i_fyqGA",
            title="justforfunc #30: The Basics of Protocol Buffers - YouTube",
            created_on=1585910095.522,
        ),
    ]


@pytest.fixture()
def test_data_dict(test_data):
    return [el.as_dict() for el in test_data]