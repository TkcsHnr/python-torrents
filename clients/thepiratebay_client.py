from clients import Client
from utils import SearchResults
from parsers import ThePirateBayParser

URL_SEARCH = "https://thepiratebay0.org/s/?page={page}&q={query}"


class ThePirateBayClient(Client):

    def __init__(self) -> None:
        super().__init__(ThePirateBayParser())

    def search(self, query: str, page: int = 1) -> SearchResults:
        try:
            response = self._client.get(
                URL_SEARCH.format(query=query, page=(page-1)))
        except Exception as e:
            raise ConnectionError(
                "Error during thepiratebay search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)
