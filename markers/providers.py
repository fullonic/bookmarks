"""List of most common bookmarkers providers.

Each one of the follow providers is resposable to fetch extra information from the url page.
This extra information can provide from a blog post title, a github project description, a 
medium article title, ect...
"""
from dataclasses import dataclass
from contextlib import suppress
from abc import ABC, abstractmethod, abstractproperty
from selectolax.parser import HTMLParser
from requests_html import HTMLSession
from markers.core import get_provider_from_url
import sys, inspect

def providers_list():
    for prov in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if "Provider" in prov[0]:
            yield prov[1]

def load_provider(url: str):
    provider_name = get_provider_from_url(url).domain
    for provider in providers_list():
        if provider.get_name() == provider_name:
            return provider
    return None



@dataclass
class BaseProvider(ABC):
    url: str
    client: object
    extra_info: str = ""

    def fetch_page(self, client) -> str:
        return client.get(url=self.url)

    @classmethod
    def get_name(cls):
        return cls.__name__.lower().strip("provider")

    @abstractmethod
    def parse_html_page(self, page) -> str:
        raise NotImplementedError

    def get_extra_info(self):
        page = self.fetch_page(client=self.client)
        self.extra_info = self.parse_html_page(page)
        return self


@dataclass
class GitHubProvider(BaseProvider):
    def parse_html_page(self, page):
        selector = ".markdown-body > p:nth-child(4)"
        tree = HTMLParser(page.text)
        with suppress(IndexError):
            return tree.css(selector)[0].text()
        return ""


@dataclass
class MartinHeinzProvider(BaseProvider):
    def parse_html_page(self, page) -> str:
        # render html page body using request_html
        page.html.render()
        tree = HTMLParser(page.html.html)
        return tree.css_first(".posttitle").text()


@dataclass
class MediumProvider(BaseProvider):
    def parse_html_page(self, page) -> str:
        tree = HTMLParser(page.text)
        return tree.css_first("h1").text()
