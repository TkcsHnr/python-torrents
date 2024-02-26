from clients import LoginClient
from parsers import ZtrackerParser
from utils import SearchResults, ZtrackerURLs, CredentialError, ConnectionError
from httpx import ReadTimeout


class ZtrackerClient(LoginClient):

    def __init__(self) -> None:
        super().__init__(ZtrackerParser(), timeout=10)

    def login(self, username: str, password: str) -> None:
        self._client.cookies.clear()
        form_data = {
            'username': username,
            'password': password
        }
        try:
            self._client.get(ZtrackerURLs.LOGIN)
            self._client.post(
                ZtrackerURLs.TAKELOGIN, data=form_data)
            response = self._client.get(ZtrackerURLs.INDEX)
        except Exception as e:
            raise ConnectionError(
                "Error during ztracker login post request!") from e

        if response.url != ZtrackerURLs.INDEX:
            self.logout()
            raise CredentialError(
                "Ztracker login post request failed, check credentials!")

        self._logged_in = True

    def search(self, query: str, page: int = 1) -> SearchResults:
        try:
            response = self._client.get(
                ZtrackerURLs.SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during ztracker search post request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
