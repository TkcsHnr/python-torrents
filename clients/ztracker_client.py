from clients import LoginClient, ClientName
from parsers import ZtrackerParser
from utils import SearchResults, CredentialError, ConnectionError

URL_BASE = "http://ztracker.cc"
URL_LOGIN = URL_BASE + "/login.php"
URL_TAKELOGIN = URL_BASE + "/takelogin.php"
URL_INDEX = URL_BASE + "/index.php"
URL_SEARCH = URL_BASE + "/browse_old.php?keywords={query}&search_type=t_name&page={page}"


class ZtrackerClient(LoginClient):

    def __init__(self) -> None:
        super().__init__(ClientName.ZTRACKER, ZtrackerParser(), timeout=20)

    def login(self, username: str, password: str) -> None:
        self._client.cookies.clear()
        form_data = {
            'username': username,
            'password': password
        }
        try:
            self._client.get(URL_LOGIN)
            self._client.post(
                URL_TAKELOGIN, data=form_data)
            response = self._client.get(URL_INDEX)
        except Exception as e:
            raise ConnectionError(
                "Error during ztracker login POST request!") from e

        if response.url != URL_INDEX:
            self.logout()
            raise CredentialError(
                "Ztracker login post request failed, check credentials!")

        self._logged_in = True

    def search(self, query: str, page: int = 1) -> SearchResults:
        try:
            response = self._client.get(
                URL_SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during ztracker search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
