from dataclasses import dataclass
from typing import NamedTuple, Optional
from urllib.parse import urlparse


@dataclass
class URLSchema:
    url: str
    scheme: Optional[str] = None
    domain: Optional[str] = None
    dot: Optional[str] = None

    def deconstruct_url(self):
        url_domain = urlparse(self.url).netloc
        self.scheme = urlparse(self.url).scheme
        if url_domain.count(".") == 1:
            self.domain, self.dot = url_domain.split(".")
            return self
        elif url_domain.count(".") == 2:
            # we need to check the url have or not a subdomain.
            # if there is '2' dots, means that we are dealing with a url with a sub domain
            # ex: docs.djangoproject.com
            self.domain, self.dot = url_domain.split(".")[1:3]
        elif url_domain.count(".") == 3:
            self.domain = url_domain.split(".")[1]
            self.dot = ".".join(url_domain.split(".")[2:])
            return self
        else:
            return Exception(f"URL format not supported {self.url}")
        return self

    def __str__(self) -> str:
        return f"{self.scheme}://{self.domain}.{self.dot}"


class SimpleURL(URLSchema):
    def __str__(self) -> str:
        return f"{self.scheme}://{self.domain}.{self.dot}"


class FaviconURL(URLSchema):
    def __str__(self) -> str:
        return f"{self.scheme}://{self.domain}.{self.dot}/favicon.ico"


def get_provider_from_url(url):
    return SimpleURL(url).deconstruct_url()


def extract_icon_from_url(url: str):
    return str(FaviconURL(url).deconstruct_url())


def get_extra_info(url):
    from .providers import load_provider

    provider = load_provider(url)
    if provider is None:
        return ""
    extra_info = provider(url).get_extra_info()
    return extra_info.extra_info


def generate_tags(url, title, tags):
    from_title = generate_tags_from_title(title, tags)
    from_url = generate_tags_from_url(url, tags)
    return set(from_title + from_url)


def generate_tags_from_url(url, tags):
    return [tag for tag in tags if tag in url]


def generate_tags_from_title(title, tags):
    return [tag for tag in tags if tag in title.lower()]
