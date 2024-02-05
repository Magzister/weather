from abc import ABC, abstractmethod
from urllib.error import URLError

from bs4 import BeautifulSoup, Tag

from app.exceptions import SSTServiceError
from app.types import Hyperlink
from app.types import Celsius
from app.utilities import Utilities as u


class SSTService(ABC):
    
    @abstractmethod
    def _get_sst(self, href: Hyperlink) -> Celsius:
        pass

    def get_sst(self, href: Hyperlink) -> Celsius:
        return self._get_sst(href)

class SeaTemperature(SSTService):

    def __init__(self) -> None:
        super().__init__()

    def _parse_sst(self, html: bytes) -> Celsius:
        soup = BeautifulSoup(html, "html.parser")
        if isinstance(div := soup.find(id="sea-temperature"), Tag):
            raw_text = div.span.get_text()
            return float(raw_text[:raw_text.index("°C")])
        else:
            raise SSTServiceError("There is no tag with "
                                  "id=\"sea-temperature\"")

    def _get_sst(self, href: Hyperlink) -> Celsius:
        try:
            html = u.make_sync_request(href)
        except URLError:
            raise SSTServiceError(f"Error while requesting {href}")
        return self._parse_sst(html)
