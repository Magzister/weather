from datetime import datetime
from unicodedata import normalize
import unicodedata
import urllib.request
from urllib.request import Request
from urllib.error import HTTPError, URLError

from app.exceptions import WebParserError
from app.types import Fahrenheit
from app.types import Celsius
from app.types import Hyperlink


class Utilities:

    @staticmethod
    def get_date() -> datetime:
        return datetime.now()

    @staticmethod
    def date_to_str(datetime: datetime, date_format: str) -> str:
        return datetime.strftime(date_format)

    @staticmethod
    def fahrenheit_to_celsius(temperature: Fahrenheit) -> Celsius:
        return (temperature - 32) * 5 / 9

    @staticmethod
    def nfc_equal(str1: str, str2: str) -> bool:
        return normalize("NFC", str1) == normalize("NFC", str2)

    @staticmethod
    def fold_equal(str1: str, str2: str) -> bool:
        return (normalize("NFC", str1).casefold() ==
                normalize("NFC", str2).casefold())

    @staticmethod
    def shave_marks(txt: str) -> str:
        norm_txt = normalize("NFD", txt)
        shaved = "".join(c for c in norm_txt
                         if not unicodedata.combining(c))
        return normalize("NFC", shaved)

    @staticmethod
    def make_sync_request(url: Hyperlink) -> bytes:
        request = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        return urllib.request.urlopen(request).read()
