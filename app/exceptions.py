class ApiServiceError(Exception):
    pass


class IPServiceError(ApiServiceError):
    pass


class LocationServiceError(ApiServiceError):
    pass


class WeatherServiceError(ApiServiceError):
    pass
