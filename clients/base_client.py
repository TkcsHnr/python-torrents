from abc import ABC, abstractmethod
from utils import SearchResults
from parsers import Parser
from utils import CredentialError
import httpx


class Client(ABC):
    def __init__(self, parser: Parser, timeout: int = 5) -> None:
        super().__init__()
        self._parser = parser
        self._client = httpx.Client(
            headers={'User-Agent': 'python-movies'}, timeout=timeout, follow_redirects=True)

    @abstractmethod
    def search(self, query: str, page: int = 1) -> SearchResults:
        pass
    
    
class LoginClient(Client):
    @staticmethod
    def _check_login(func):
        def wrapper(self, *args, **kwargs):
            if not self._logged_in:
                raise CredentialError(
                    f"{self.__name__} needs to be logged in before usage!")

            return func(self, *args, **kwargs)

        return wrapper
    
    def __init__(self, parser: Parser, timeout: int = 1) -> None:
        super().__init__(parser, timeout=timeout)
        self._logged_in = False

    @abstractmethod
    def login(self, username: str, password: str) -> None:
        pass
    
    def logout(self) -> None:
        self._client.cookies.clear()
        self._client.close()
        self._logged_in = False

    @_check_login
    @abstractmethod
    def search(self, query: str, page: int = 1) -> SearchResults:
        pass
