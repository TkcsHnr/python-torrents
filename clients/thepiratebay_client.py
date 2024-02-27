from clients import Client
from utils import SearchResults, ThePirateBayURLs
from parsers import ThePirateBayParser

class ThePirateBayClient(Client):
    
    def __init__(self) -> None:
        super().__init__(ThePirateBayParser())
    
    def search(self, query: str, page: int = 0) -> SearchResults:
        try:
            response = self._client.get(
                ThePirateBayURLs.SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during thepiratebay search post request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)