class ApiServiceError(Exception):
    pass


class IPServiceError(ApiServiceError):
    pass


class LocationServiceError(ApiServiceError):
    pass


class WeatherServiceError(ApiServiceError):
    pass


class DBError(Exception):
    pass


class NoResultError(DBError):
    pass


class MultipleResultsError(DBError):
    pass
