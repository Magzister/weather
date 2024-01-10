from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from json.decoder import JSONDecodeError
from typing import NamedTuple
import urllib.request
from urllib.error import URLError

import config
from exceptions import ApiServiceError
from ip_service import IP


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


@dataclass(slots=True, frozen=True)
class Location:
    country: str
    city: str
    coordinates: Coordinates


class LocationService(ABC):

    @abstractmethod
    def _fetch_location(self, ip: IP) -> Location:
        pass

    def get_location(self, ip: IP) -> Location:
        return self._fetch_location(ip)


class Ipapi(LocationService):

    def __init__(self) -> None:
        super().__init__()

    def _get_ipapi_response(self, ip: IP) -> bytes:
        response_format = config.IPAPI_FORMAT
        url = config.IPAPI_URL.format(
                ip=ip, response_format=response_format)
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise ApiServiceError

    def _parse_country(self, response_dict: dict) -> str:
        return response_dict["country_name"]

    def _parse_city(self, response_dict: dict) -> str:
        return response_dict["city"]

    def _parse_coordinates(self, response_dict: dict) -> Coordinates:
        return Coordinates(
                latitude=response_dict["latitude"],
                longitude=response_dict["longitude"]
        )

    def _parse_ipapi_response(self, response: bytes) -> Location:
        try:
            response_dict = json.loads(response)
        except JSONDecodeError:
            raise ApiServiceError
        return Location(
            country=self._parse_country(response_dict),
            city=self._parse_city(response_dict),
            coordinates=self._parse_coordinates(response_dict)
        )

    def _fetch_location(self, ip: IP) -> Location:
        ipapi_response = self._get_ipapi_response(ip)
        return self._parse_ipapi_response(ipapi_response)


if __name__ == "__main__":
    from ip_service import Ifconfig
    ip = Ifconfig().get_ip()
    print(Ipapi().get_location(ip))
