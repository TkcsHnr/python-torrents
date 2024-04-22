from parsers import Parser
from bs4 import Tag
from utils import Torrent
import re

URL_DOWNLOAD = "https://estone.cc/download.php?id={id}&name=[eStone]{title}.torrent"


class EstoneParser(Parser):
    def __init__(self) -> None:
        super().__init__()
        self._id_pattern = re.compile(r'torrent_(\d+)')

    def get_torrents(self):
        torrent_boxes = self._soup.find_all(
            "div", id=re.compile(r'torrent_\d+'))

        for box in torrent_boxes:
            tagbox: Tag = box
            data_container = tagbox.select_one('div > div:nth-child(3)')

            id = self._id_pattern.search(tagbox.get('id'))[1]
            link_tag = data_container.select_one(
                'div:first-child > div > a:last-of-type')
            title = link_tag.get('title')
            size = data_container.select_one(
                'div:nth-child(5) > div').text.strip()
            seed = data_container.select_one('div:nth-child(6) > div > a').text
            leech = data_container.select_one(
                'div:nth-child(7) > div > a').text
            download = URL_DOWNLOAD.format(id=id, title=title)

            yield Torrent(int(id), title, size, int(seed), int(leech), download=download)

    def get_page_count(self) -> int:
        paginator = self._soup.select_one('#kozep_hatter > center > b')

        if not paginator:
            return 0

        nth_last_index = 1
        next_button = paginator.select_one('a:last-child > img')
        if next_button:
            nth_last_index = 2

        last_page_tag = paginator.select_one(
            f'a:nth-last-child({nth_last_index})')
        first_number = int(last_page_tag.text.split('-')[0])

        return first_number // 50 + 1
