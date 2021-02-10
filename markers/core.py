from typing import NamedTuple
from urllib.parse import urlparse


class FaviconURL(NamedTuple):
    scheme: str
    domain: str
    dot: str

    def __str__(self) -> str:
        return f"{self.scheme}://{self.domain}.{self.dot}/favicon.ico"


def generate_tags(url, title, tags):
    from_title = generate_tags_from_title(title, tags)
    from_url = generate_tags_from_url(url, tags)
    return set(from_title + from_url)


def generate_tags_from_url(url, tags):
    return [tag for tag in tags if tag in url]


def generate_tags_from_title(title, tags):
    return [tag for tag in tags if tag in title.lower()]


def normalize_url(url: str):
    url_domain = urlparse(url).netloc
    scheme = urlparse(url).scheme
    if url_domain.count(".") == 2:
        # we need to check the url have or not a subdomain.
        # if there is '2' dots, means that we are dealing with a url with a sub domain
        # ex: docs.djangoproject.com
        return FaviconURL(scheme, *url_domain.split(".")[1:])
    elif url_domain.count(".") == 3:
        return FaviconURL(
            scheme, url_domain.split(".")[1], ".".join(url_domain.split(".")[2:])
        )

    return FaviconURL(scheme, *url_domain.split("."))


def extract_icon_from_url(url: str):
    favicon = normalize_url(url)
    return str(favicon)
