from utils import Torrent
from dataclasses import dataclass

@dataclass
class SearchResults:
    torrents: list[Torrent]
    page_count: int
    current_page: int