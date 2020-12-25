import os
import pytest


def pytest_configure():
    """
    Use for override default settings
    https://pytest-django.readthedocs.io/en/latest/configuring_django.html#using-django-conf-settings-configure
    """
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookmarks.settings")
