from datetime import datetime
from typing import TypeAlias
from unicodedata import normalize


Fahrenheit: TypeAlias = float
Celsius: TypeAlias = float


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
