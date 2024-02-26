from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


class Parser(ABC):
    def feed(self, data: str) -> None:
        self._soup = BeautifulSoup(data, "lxml")

    @abstractmethod
    def get_torrents(self):
        pass

    @abstractmethod
    def get_page_count(self) -> int:
        pass
