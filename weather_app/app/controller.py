from app.ip_service import IPService
from app.location_service import IPLocationService
from app.location_service import ReverseGeocodingService
from app.weather_service import WeatherService
from app.types import IP
from app.types import Location
from app.types import Weather
from app.types import Coordinates
from app.exceptions import IPServiceError
from app.exceptions import LocationServiceError
from app.exceptions import WeatherServiceError


class Controller:

    def __init__(self,
                 ip_service: IPService,
                 location_service: IPLocationService,
                 reverse_geocoding_service: ReverseGeocodingService,
                 weather_service: WeatherService) -> None:
        self._ip_service = ip_service
        self._location_service = location_service
        self._reverse_geocoding_service = reverse_geocoding_service
        self._weather_service = weather_service

    @property
    def ip_service(self):
        return self._ip_service

    @ip_service.setter
    def ip_service(self, ip_service: IPService):
        self._ip_service = ip_service

    @property
    def location_service(self):
        return self._location_service

    @location_service.setter
    def location_service(self, location_service: IPLocationService):
        self._location_service = location_service

    @property
    def weather_service(self):
        return self._weather_service

    @weather_service.setter
    def weather_service(self, weather_service: WeatherService):
        self._weather_service = weather_service

    def _get_ip(self) -> IP:
        try:
            return self._ip_service.get_ip()
        except IPServiceError as err:
            print("Can't get information form ip service.")
            raise err

    def _get_ip_location(self, ip: IP) -> Location:
        try:
            return self._location_service.get_location(ip)
        except LocationServiceError as err:
            print("Can't get information form location service.")
            raise err

    def _get_coords_location(self, coords: Coordinates) -> Location:
        try:
            return self._reverse_geocoding_service.get_address(coords)
        except LocationServiceError as err:
            print("Can't get information from reverse geocoding service.")
            raise err
    
    def _get_weather(self, coords: Coordinates) -> Weather:
        try:
            return self._weather_service.get_weather(coords)
        except WeatherServiceError as err:
            print("Can't get information form weather service.")
            raise err

    def get_weather_by_ip(self) -> tuple[Location, Weather]:
        ip = self._get_ip()
        location = self._get_ip_location(ip)
        weather = self._get_weather(location.coordinates)
        return location, weather

    def get_weather_by_coords(self, coords: Coordinates
                              ) -> tuple[Location, Weather]:
        location = self._get_coords_location(coords)
        weather = self._get_weather(location.coordinates)
        return location, weather
