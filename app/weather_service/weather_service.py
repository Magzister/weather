from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import json
from json.decoder import JSONDecodeError
from typing import Literal
import urllib.request
from urllib.error import URLError

from app import config
from app.exceptions import WeatherServiceError
from app.types import Coordinates
from app.types import Fahrenheit
from app.types import Celsius
from app.types import Weather
from app.utilities import Utilities as u


class WeatherService(ABC):

    @abstractmethod
    def _fetch_weather(self, coords: Coordinates) -> Weather:
        pass

    def get_weather(self, coords: Coordinates) -> Weather:
        '''
        Return weather information.
        Public method.
        Must be used by client code.
        '''
        return self._fetch_weather(coords)


class VisualCrossing(WeatherService):

    def __init__(self) -> None:
        super().__init__()

    def _get_visualcrossing_response(self, coords: Coordinates) -> bytes:
        date = u.get_date()
        date_str = u.date_to_str(date, config.DATE_FORMAT)
        lat, lon = coords
        url = config.VISUALCROSSING_URL.format(
            latitude=lat,
            longitude=lon,
            date=date_str
        )
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise WeatherServiceError("Error while requesting weather information")

    def _fahrenheit_to_celsius(self, temperature: Fahrenheit) -> Celsius:
        return (temperature - 32) * 5 / 9

    def _parse_temperature(
            self,
            response_dict: dict,
            type_: Literal["temp", "feelslike"]) -> Celsius:
        return u.fahrenheit_to_celsius(response_dict["days"][0][type_])

    def _parse_description(self, response_dict: dict) -> str:
        return response_dict["days"][0]["description"]

    def _parse_sun_time(
            self,
            response_dict: dict,
            type_: Literal["sunriseEpoch", "sunsetEpoch"]) -> datetime:
        return datetime.fromtimestamp(response_dict["days"][0][type_])

    def _parse_visualcrossing_response(self, response: bytes) -> Weather:
        try:
            response_dict = json.loads(response)
        except JSONDecodeError:
            raise WeatherServiceError("Error while parsing resporse")
        return Weather(
            temperature=self._parse_temperature(response_dict, "temp"),
            feelslike=self._parse_temperature(response_dict, "feelslike"),
            description=self._parse_description(response_dict),
            sunrise=self._parse_sun_time(response_dict, "sunriseEpoch"),
            sunset=self._parse_sun_time(response_dict, "sunsetEpoch")
        )

    def _fetch_weather(self, coords: Coordinates) -> Weather:
        visualcrossing_response = self._get_visualcrossing_response(coords)
        return self._parse_visualcrossing_response(visualcrossing_response)


if __name__ == "__main__":
    from app.ip_service import Ifconfig
    from app.location_service import Ipapi
    ip = Ifconfig().get_ip()
    location = Ipapi().get_location(ip)
    weather = VisualCrossing().get_weather(location.coordinates)
    print(weather)
