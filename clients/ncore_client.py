from clients import LoginClient, ClientName
from parsers import NcoreParser
from utils import SearchResults, CredentialError, ConnectionError, TooShortQueryError

URL_BASE = "https://ncore.pro"
URL_INDEX = URL_BASE + "/index.php"
URL_LOGIN = URL_BASE + "/login.php"
URL_SEARCH = URL_BASE + "/torrents.php?mire={query}&oldal={page}"


class NcoreClient(LoginClient):
    def __init__(self) -> None:
        super().__init__(ClientName.NCORE, NcoreParser())

    def login(self, username: str, password: str):
        self._client.cookies.clear()
        form_data = {
            'nev': username,
            'pass': password
        }
        try:
            response = self._client.post(URL_LOGIN, data=form_data)
        except Exception as e:
            raise ConnectionError(
                "Error during ncore login POST request, check internet connection!") from e

        if response.url != URL_INDEX:
            self.logout()
            raise CredentialError(
                "Error during ncore login, check credentials!")

        self._logged_in = True

    def search(self, query: str, page: int = 1):
        if len(query) < 3:
            raise TooShortQueryError("The search query should be at least 3 characters long!")

        try:
            response = self._client.get(
                URL_SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during ncore search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
