from abc import ABC, abstractmethod
import urllib.request
from urllib.request import Request
import urllib.parse
from urllib.error import HTTPError, URLError

from app import config
from app.exceptions import WebParserError
from bs4 import BeautifulSoup, Tag
from typing import NamedTuple


class CountryHref(NamedTuple):
    country: str
    href: str


class SST(NamedTuple):
    country: str
    city: str
    href: str


class SSTWebParser(ABC):

    @abstractmethod
    def _parse(self) -> list[SST]:
        pass

    def parse(self) -> list[SST]:
        return self._parse()


class SeaTemperature(SSTWebParser):

    def __init__(self) -> None:
        super().__init__()

    def _get_html(self, url: str) -> bytes:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        try:
            return urllib.request.urlopen(request).read()
        except HTTPError as err:
            raise err
        except URLError:
            raise WebParserError(f"Error while requesting {url} html")

    def _parse_a_tag(self, a: Tag) -> tuple[str, str]:
        text = a.get_text()
        href = a.get("href")
        if not isinstance(href, str):
            raise WebParserError("Hyperlink {href} is not a string")
        return text, href

    def _get_countryhref_list(self,
                               soup: Tag
                               ) -> list[CountryHref]:
        if isinstance(div := soup.find(id="main-home"), Tag):
            li_list = div.find_all("li")
        else:
            raise WebParserError("There is no tag with id=\"main-home\", "
                                 f"visit {config.SEA_TEMPERATURE_URL}")
        countryhref_list = list()
        for li in li_list:
            country, href = self._parse_a_tag(li.a)
            href = urllib.parse.urljoin(config.SEA_TEMPERATURE_URL, href)
            countryhref_list.append(CountryHref(country=country, href=href))
        return countryhref_list

    def _get_sst_list(self, countryhref_list: list[CountryHref]) -> list[SST]:
        sst_list = list()
        for countryhref in countryhref_list:
            country, href = countryhref
            try:
                html = self._get_html(href)
            except HTTPError as err:
                match err.code:
                    case 404: continue
                    case _: raise err
            soup = BeautifulSoup(html, "html.parser")
            if isinstance(ul := soup.find(id="location-list"), Tag):
                li_list = ul.find_all("li")
            else:
                raise WebParserError("There is no tag with "
                                     f"id=\"location-list\", visit {href}")
            for li in li_list:
                city, href = self._parse_a_tag(li.a)
                href = urllib.parse.urljoin(config.SEA_TEMPERATURE_URL, href)
                sst_list.append(SST(country=country, city=city, href=href))
        return sst_list

    def _parse(self) -> list[SST]:
        html = self._get_html(config.SEA_TEMPERATURE_URL)
        soup = BeautifulSoup(html, "html.parser")
        countryhref_list = self._get_countryhref_list(soup)
        return self._get_sst_list(countryhref_list)
