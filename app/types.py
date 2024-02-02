from datetime import datetime
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias
from typing import NamedTuple


IP: TypeAlias = str
Hyperlink: TypeAlias = str
Fahrenheit: TypeAlias = float
Celsius: TypeAlias = float


class Command(str, Enum):
    CREATE_SST_DATABASE = "createsstdb"
    SEA_TEMPERATURE = "seatemperature"
    NO_COMMAND = ""


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


@dataclass(slots=True, frozen=True)
class Location:
    country: str
    city: str
    coordinates: Coordinates


@dataclass(slots=True, frozen=True)
class Weather:
    temperature: Celsius
    feelslike: Celsius
    description: str
    sunrise: datetime
    sunset: datetime


class CountryHref(NamedTuple):
    country: str
    href: str


@dataclass(slots=True, frozen=True)
class SST:
    country: str
    city: str
    href: str
