from abc import ABC, abstractmethod
import urllib.request
from urllib.error import URLError

from app import config
from app.exceptions import IPServiceError
from app.types import IP


class IPService(ABC):

    @abstractmethod
    def _fetch_ip(self) -> IP:
        pass

    def get_ip(self) -> IP:
        '''Return IP adress. Public method. Must be used from client code.'''
        return self._fetch_ip()


class Ifconfig(IPService):

    def __init__(self) -> None:
        super().__init__()

    def _get_ifconfig_response(self) -> bytes:
        '''
        Return response with ip from ifconfig.me.
        Response has bytes type.
        '''
        url = config.IFCONFIG_URL
        try:
            return urllib.request.urlopen(url).read()
        except URLError:
            raise IPServiceError("Error while requesting ip adress")

    def _parse_ip(self, response: bytes) -> IP:
        '''Convert IP in response from bytes to str'''
        return response.decode("utf-8")

    def _fetch_ip(self) -> IP:
        ifconfig_response = self._get_ifconfig_response()
        return self._parse_ip(ifconfig_response)


if __name__ == "__main__":
    print(Ifconfig().get_ip())
