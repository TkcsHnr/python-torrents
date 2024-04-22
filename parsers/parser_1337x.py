from parsers import Parser
from utils import Torrent
import re
from bs4 import BeautifulSoup


class Parser1337x(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._id_pattern = re.compile(r'/torrent/(\d+)')

    def get_torrents(self):
        rows = self._soup.select(
            'div.inner-table > div.table-list-wrap > table > tbody > tr')

        for row in rows:
            link_tag = row.select_one('td.name > a:not(.icon)')

            id = self._id_pattern.search(link_tag.get('href'))[1]
            title = link_tag.text

            seed = row.select_one('td.seeds').text
            leech = row.select_one('td.leeches').text
            size = row.select_one('td.size').text

            yield Torrent(int(id), title, size, int(seed), int(leech))

        return []

    def get_page_count(self) -> int:
        table_exists = self._soup.select_one(
            'div.inner-table > div.table-list-wrap > table > tbody > tr')
        if not table_exists:
            return 0

        paginator = self._soup.select_one('.pagination')

        if not paginator:
            return 1

        last_link = paginator.select_one('ul li:last-child')
        return int(last_link.text)


class MagnetLink1337xParser:
    def feed(self, data: str) -> None:
        self._soup = BeautifulSoup(data, "lxml")

    def get_magnet_link(self, id: int) -> str:
        download_button = self._soup.select_one('.torrentdown1')

        magnet_link = download_button.get('href')

        return magnet_link
