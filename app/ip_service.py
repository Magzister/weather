from abc import ABC, abstractmethod
from typing import TypeAlias


IP: TypeAlias = str


class IPService(ABC):
    @abstractmethod
    def _fetch_api(self) -> IP:
        pass

    def get_ip(self) -> IP:
        return self._fetch_api()
