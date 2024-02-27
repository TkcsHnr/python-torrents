from parsers import Parser
from utils import ZtrackerURLs, Torrent
import re


class ZtrackerParser(Parser):

    def __init__(self) -> None:
        super().__init__()
        self._id_pattern = re.compile(r'id=(\d+)')
        self._title_pattern = re.compile(r'<font.*?>(.*?)</font>')
        self._page_pattern = re.compile(r'- (\d+)')

    def get_torrents(self):
        # best way to find the main torrents table because NOTHING has class names
        attributes = {'border': '1', 'cellspacing': '0',
                      'cellpadding': '0', 'width': '100%'}
        torrents_table = self._soup.find('table', attrs=attributes)
        
        if not torrents_table:
            return []

        rows = torrents_table.select('tr:not(:first-child):not(:last-child)')

        for row in rows:
            link_tag = row.select_one('td:nth-child(2) a')
            id = self._id_pattern.search(link_tag.get('href'))[1]
            title = self._title_pattern.search(
                link_tag.get('onmouseover'))[1]

            size_td = row.select_one('td:nth-last-child(2)')
            size = size_td.text.replace('+', '').strip()
            seed = row.select_one('td:nth-child(7)').text
            leech = row.select_one('td:nth-child(8)').text
            download = ZtrackerURLs.DOWNLOAD.format(id=id)

            yield Torrent(int(id), title, size, int(seed), int(leech), download)

    def get_page_count(self) -> int:
        not_found = self._soup.select_one('div.error')
        if not_found:
            return 0
        
        paginator = self._soup.select_one('#navcontainer_f')
        if not paginator:
            return 1

        pages_from_to = paginator.select_one('ul li:first-child')
        page_count = self._page_pattern.search(pages_from_to.text)[1]

        return int(page_count)
