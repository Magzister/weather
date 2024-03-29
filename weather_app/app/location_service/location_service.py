from abc import ABC, abstractmethod
from dataclasses import dataclass
import json
from json.decoder import JSONDecodeError
from typing import NamedTuple
import urllib.request
from urllib.error import URLError

from app import config
from app.exceptions import LocationServiceError
from app.types import IP
from app.types import Coordinates
from app.types import Location


class IPLocationService(ABC):

    @abstractmethod
    def _fetch_location(self, ip: IP) -> Location:
        pass

    def get_location(self, ip: IP) -> Location:
        '''
        Return location info by ip adress.
        Public method.
        Must be used by client code.
        '''
        return self._fetch_location(ip)


class ReverseGeocodingService(ABC):

    @abstractmethod
    def _fetch_address(self, coords: Coordinates) -> Location:
        pass

    def get_address(self, coords: Coordinates) -> Location:
        return self._fetch_address(coords)


class Ipapi(IPLocationService):
    '''
    ipapi.co location service.
    Supports only json data format for now.
    '''

    def __init__(self) -> None:
        super().__init__()

    def _get_ipapi_response(self, ip: IP) -> bytes:
        '''
        Return response from ipapi service with location info.
        Response is a json and has bytes type.
        '''
        response_format = config.IPAPI_FORMAT
        url = config.IPAPI_URL.format(
                ip=ip, response_format=response_format)
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise LocationServiceError("Error while requesting "
                                       "location information")

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
        '''
        Transform bytes response to dict and parse it to Location dataclass.
        Return Location object.
        '''
        try:
            response_dict = json.loads(response)
        except JSONDecodeError:
            raise LocationServiceError("Error while parsing location response")
        return Location(
            country=self._parse_country(response_dict),
            city=self._parse_city(response_dict),
            coordinates=self._parse_coordinates(response_dict)
        )

    def _fetch_location(self, ip: IP) -> Location:
        ipapi_response = self._get_ipapi_response(ip)
        return self._parse_ipapi_response(ipapi_response)


class Geoapify(ReverseGeocodingService):

    def _get_geoapify_response(self, coords: Coordinates) -> bytes:
        url = config.GEOAPIFY_URL.format(latitude=coords.latitude,
                                         longitude = coords.longitude)
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise LocationServiceError("Error while requesting "
                                       "address information")

    def _parse_city(self, response_dict: dict) -> str:
        return response_dict["city"]

    def _parse_country(self, response_dict: dict) -> str:
        return response_dict["country"]

    def _parse_geoapify_response(self,
                                 response: bytes,
                                 coords: Coordinates) -> Location:
        try:
            response_dict = json.loads(response)
        except JSONDecodeError:
            raise LocationServiceError("Error while parsing address response")
        response_dict = response_dict["features"][0]["properties"]
        return Location(
            country=self._parse_country(response_dict),
            city=self._parse_city(response_dict),
            coordinates=coords
        )

    def _fetch_address(self, coords: Coordinates) -> Location:
        geoapify_response = self._get_geoapify_response(coords)
        return self._parse_geoapify_response(geoapify_response, coords)


if __name__ == "__main__":
    from ip_service import Ifconfig
    ip = Ifconfig().get_ip()
    print(Ipapi().get_location(ip))
