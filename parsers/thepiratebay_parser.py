from parsers import Parser
import re
from math import ceil
from utils import Torrent


class ThePirateBayParser(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._torrent_found_pattern = re.compile(r'\(approx (\d+) found\)')
        self._id_pattern = re.compile(r'torrent/(\d+)')
        self._size_pattern = re.compile(r'Size (.*?),')

    def get_torrents(self):
        # last row is paginator
        rows = self._soup.select(
            '#searchResult > tbody > tr, #searchResult > tr')

        for row in rows:
            link_tag = row.select_one('.detLink')

            # paginator row
            if not link_tag:
                continue

            id = self._id_pattern.search(link_tag.attrs.get('href'))[1]
            title = link_tag.attrs.get('title')

            desc = row.select_one('.detDesc')
            size = self._size_pattern.search(desc.text)[1]

            seed = row.select_one('td:nth-last-child(2)').text
            leech = row.select_one('td:last-child').text

            magnet_link = row.select_one('td:nth-child(2) > a')
            download = magnet_link.attrs.get('href')

            yield (Torrent(int(id), title, size, int(seed), int(leech), download))

        return []

    def get_page_count(self) -> int:
        h2 = self._soup.select_one('body > h2')

        torrent_found = self._torrent_found_pattern.search(h2.text)[1]
        return ceil(int(torrent_found) / 30)
