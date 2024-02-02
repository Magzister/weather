class ApiServiceError(Exception):
    pass


class IPServiceError(ApiServiceError):
    pass


class LocationServiceError(ApiServiceError):
    pass


class WeatherServiceError(ApiServiceError):
    pass


class ParserError(Exception):
    pass


class WebParserError(ParserError):
    pass


class SSTServiceError(ParserError):
    pass


class DBError(Exception):
    pass


class NoResultError(DBError):
    pass


class MultipleResultsError(DBError):
    pass
