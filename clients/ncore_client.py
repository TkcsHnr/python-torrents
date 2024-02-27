from clients import LoginClient
from parsers import NcoreParser
from utils import SearchResults, NcoreURLs, CredentialError, ConnectionError


class NcoreClient(LoginClient):
    def __init__(self) -> None:
        super().__init__(NcoreParser())

    def login(self, username: str, password: str):
        self._client.cookies.clear()
        form_data = {
            'nev': username,
            'pass': password
        }
        try:
            response = self._client.post(NcoreURLs.LOGIN, data=form_data)
        except Exception as e:
            raise ConnectionError(
                "Error during ncore login POST request, check internet connection!") from e

        if response.url != NcoreURLs.INDEX:
            self.logout()
            raise CredentialError(
                "Error during ncore login, check credentials!")

        self._logged_in = True

    def search(self, query: str, page: int = 1):
        if len(query) < 3:
            return

        try:
            response = self._client.get(
                NcoreURLs.SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during ncore search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
