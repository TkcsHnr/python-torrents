from clients import LoginClient, ClientName
from parsers import EstoneParser
from utils import SearchResults, CredentialError, ConnectionError


URL_BASE = "https://estone.cc"
URL_LOGIN = URL_BASE + "/login.php"
URL_INDEX = URL_BASE + "/"
URL_SEARCH = URL_BASE + "/bongeszo.php?kereses_nev={query}&lap={page}"


class EstoneClient(LoginClient):
    def __init__(self) -> None:
        super().__init__(ClientName.ESTONE, EstoneParser(), timeout=10)

    def login(self, username: str, password: str):
        self._client.cookies.clear()
        headers = {
            'Referer': URL_LOGIN
        }
        form_data = {
            'login_username': username,
            'login_password': password,
            'returnto': '/'
        }

        try:
            response = self._client.post(
                URL_LOGIN, headers=headers, data=form_data)
        except Exception as e:
            raise ConnectionError(
                "Error during estone login POST request, check internet connection!") from e

        if response.url != URL_INDEX:
            self.logout()
            raise CredentialError(
                "Error during estone login, check credentials!")

        self._logged_in = True

    def search(self, query: str, page: int = 1):
        try:
            response = self._client.get(
                URL_SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during estone search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
