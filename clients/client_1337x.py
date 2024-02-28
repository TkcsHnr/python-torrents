from clients import Client
from utils import SearchResults
from parsers import Parser1337x, MagnetLink1337xParser

URL_BASE = "https://www.1377x.to"
URL_SEARCH = URL_BASE + "/search/{query}/{page}/"
URL_TORRENT = URL_BASE + "/torrent/{id}/d"


class Client1337x(Client):

    def __init__(self) -> None:
        super().__init__(Parser1337x())
        self._magnet_link_parser = MagnetLink1337xParser()

    def search(self, query: str, page: int = 1) -> SearchResults:
        try:
            response = self._client.get(
                URL_SEARCH.format(query=query, page=page))
        except Exception as e:
            raise ConnectionError(
                "Error during 1337x search GET request, check internet connection!") from e

        self._parser.feed(response.text)

        torrents = [t for t in self._parser.get_torrents()]
        page_count = self._parser.get_page_count()

        return SearchResults(torrents, page_count, page)

    def get_magnet_link(self, id: int) -> str:
        try:
            response = self._client.get(
                URL_TORRENT.format(id=id))
        except Exception as e:
            raise ConnectionError(
                "Error during 1337x magnet link search GET request, check internet connection!") from e

        self._magnet_link_parser.feed(response.text)

        return self._magnet_link_parser.get_magnet_link(id)
