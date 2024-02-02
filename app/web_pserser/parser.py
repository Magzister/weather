from abc import ABC, abstractmethod
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

from app import config
from app.exceptions import WebParserError
from app.types import CountryHref
from app.types import SST
from app.utilities import Utilities as u
from bs4 import BeautifulSoup, Tag


class SSTWebParser(ABC):

    @abstractmethod
    def _parse(self) -> list[SST]:
        pass

    def parse(self) -> list[SST]:
        return self._parse()


class SeaTemperature(SSTWebParser):

    def __init__(self) -> None:
        super().__init__()

    def _parse_a_tag(self, a: Tag) -> tuple[str, str]:
        text = a.get_text().strip()
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
                html = u.make_sync_request(href)
            except HTTPError as err:
                match err.code:
                    case 404: continue
                    case _: raise err
            except URLError:
                raise WebParserError(f"Error while requesting {href}")
            soup = BeautifulSoup(html, "html.parser")
            if isinstance(ul := soup.find(id="location-list"), Tag):
                li_list = ul.find_all("li")
            else:
                raise WebParserError("There is no tag with "
                                     f"id=\"location-list\", visit {href}")
            for li in li_list:
                city, href = self._parse_a_tag(li.a)
                href = urllib.parse.urljoin(config.SEA_TEMPERATURE_URL, href)
                country = u.shave_marks(country)
                city = u.shave_marks(city)
                sst_list.append(SST(country=country, city=city, href=href))
        return sst_list

    def _parse(self) -> list[SST]:
        html = u.make_sync_request(config.SEA_TEMPERATURE_URL)
        soup = BeautifulSoup(html, "html.parser")
        countryhref_list = self._get_countryhref_list(soup)
        return self._get_sst_list(countryhref_list)
