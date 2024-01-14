from datetime import datetime
from typing import TypeAlias


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
