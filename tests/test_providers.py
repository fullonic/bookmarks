from markers.core import get_extra_info, get_provider_from_url
from markers.providers import (
    GitHubProvider,
    MartinHeinzProvider,
    MediumProvider,
    load_provider,
)
import pytest
import httpx
from requests_html import HTMLSession


@pytest.fixture
def github_provider():
    return GitHubProvider("https://github.com/rushter/selectolax")


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
    github = GitHubProvider(url)
    github.get_extra_info()
    assert isinstance(github.extra_info, str)

@pytest.mark.skip  # TODO: How to install and run chrome on docker
def test_martin_heinz_provider():
    url = "https://martinheinz.dev/blog/42"
    client = HTMLSession()
    mheinz = MartinHeinzProvider(url)
    assert mheinz.get_extra_info().extra_info == "Building Docker Images The Proper Way"


@pytest.mark.vcr
def test_medium_provider():
    url = "https://medium.com/poka-techblog/5-different-ways-to-backup-your-postgresql-database-using-python-3f06cea4f51"
    medium = MediumProvider(url=url)
    assert (
        medium.get_extra_info().extra_info
        == "5 different ways to backup your PostgreSQL database using Python"
    )


def test_automatically_generate_provider_name():
    assert MediumProvider.get_name() == "medium"


@pytest.mark.parametrize(
    "url, provider_name",
    [
        ("https://github.com/rushter/selectolax", "github"),
        ("https://martinheinz.dev/blog/42", "martinheinz"),
    ],
)
def test_get_provider_from_url_domain(url, provider_name):
    provider = get_provider_from_url(url)
    assert provider.domain == provider_name


def test_load_provider_using_url_domain():
    provider = load_provider("https://github.com/rushter/selectolax")
    assert issubclass(provider, GitHubProvider)


def test_get_extra_data_process():
    extra_info = get_extra_info("https://github.com/rushter/selectolax")
    expected = "A fast HTML5 parser with CSS selectors using Modest engine."
    assert extra_info == expected
