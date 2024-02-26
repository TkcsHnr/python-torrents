from parsers import Parser
from bs4 import BeautifulSoup
from utils import Torrent, NcoreURLs, NcoreKeyNotFoundError
import re

class NcoreParser(Parser):
    def __init__(self) -> None:
        super().__init__()
        self._id_pattern = re.compile(r'id=(\d+)')
        self._page_pattern = re.compile(r'oldal=(\d+)')
    
    @staticmethod
    def _get_key(soup: BeautifulSoup) -> str:
        key_link = soup.find("link", {"rel": "alternate"})
        if key_link:
            return key_link.get("href").split("=")[1]
        raise NcoreKeyNotFoundError("Couldn't find the unique key needed for downloading torrents!")

    def get_torrents(self):
        boxes = self._soup.find_all("div", {"class": ["box_nagy", "box_nagy2"]})

        key = self._get_key(self._soup)
        for box in boxes:
            link_tag = box.find(
                "div", {"class": ["torrent_txt", "torrent_txt2"]}).find("a")
            id = self._id_pattern.search(link_tag.get("href"))[1]
            title = link_tag.get("title")
            size = box.find(
                "div", {"class": ["box_meret", "box_meret2"]}).string
            seed = box.find("div", {"class": ["box_s", "box_s2"]}).string
            leech = box.find("div", {"class": ["box_l", "box_l2"]}).string
            download_link = NcoreURLs.DOWNLOAD.format(id=id, key=key)

            yield Torrent(int(id), title, size, int(seed), int(leech), download_link)

    def get_page_count(self) -> int:
        pager_top = self._soup.select_one("#pager_top")
        if not pager_top:
            return 0
        last_page_tag = pager_top.select_one("*:nth-last-child(2)")
        if last_page_tag.name == "a":
            last_page = int(self._page_pattern.search(last_page_tag.get("href"))[1])
        else:
            last_page = int(last_page_tag.string.split("-")[0]) // 25 + 1
        return last_page
