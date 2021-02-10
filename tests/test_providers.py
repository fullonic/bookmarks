from markers.providers import GitHub, MartinHeinz, Medium
import pytest
import httpx
from requests_html import HTMLSession


@pytest.fixture
def github_provider():
    return GitHub("https://github.com/rushter/selectolax", client=httpx)


@pytest.mark.vcr
def test_provider_page_text(github_provider):
    assert isinstance(github_provider.fetch_page(), str)


@pytest.mark.vcr
def test_provider_page_text(github_provider):
    github_provider.get_extra_info()
    assert isinstance(github_provider.extra_info, str)
    assert (
        github_provider.extra_info
        == "A fast HTML5 parser with CSS selectors using Modest engine."
    )


@pytest.mark.parametrize(
    "url",
    (
        "https://github.com/rushter/selectolax",
        "https://github.com/python-visualization/folium",
        "https://github.com/miguelgrinberg/microflack_tokens",
    ),
)
def test_general_github(url):
    github = GitHub(url, client=httpx)
    github.get_extra_info()
    assert isinstance(github.extra_info, str)


def test_martin_heinz_provider():
    url = "https://martinheinz.dev/blog/42"
    client = HTMLSession()
    mheinz = MartinHeinz(url, client=client)
    assert mheinz.get_extra_info().extra_info == "Building Docker Images The Proper Way"


@pytest.mark.vcr
def test_medium_provider():
    url = "https://medium.com/poka-techblog/5-different-ways-to-backup-your-postgresql-database-using-python-3f06cea4f51"
    medium = Medium(url=url, client=httpx)
    assert (
        medium.get_extra_info().extra_info
        == "5 different ways to backup your PostgreSQL database using Python"
    )
