class NcoreURLs:
    BASE = "https://ncore.pro"
    INDEX = BASE + "/index.php"
    LOGIN = BASE + "/login.php"
    SEARCH = BASE + "/torrents.php?mire={query}&oldal={page}"
    DOWNLOAD = BASE + "/torrents.php?action=download&id={id}&key={key}"


class ZtrackerURLs:
    BASE = "http://ztracker.cc"
    LOGIN = BASE + "/login.php"
    TAKELOGIN = BASE + "/takelogin.php"
    INDEX = BASE + "/index.php"
    SEARCH = BASE + "/browse_old.php?keywords={query}&search_type=t_name&page={page}"
    DOWNLOAD = BASE + "/download.php?id={id}"
    
    
class EstoneURLs:
    BASE = "https://estone.cc"
    LOGIN = BASE + "/login.php"
    INDEX = BASE + "/"
    SEARCH = BASE + "/bongeszo.php?kereses_nev={query}&lap={page}"
    DOWNLOAD = BASE + "/download.php?id={id}&name={title}.torrent"


class ThePirateBayURLs:
    SEARCH = "https://thepiratebay0.org/s/?page={page}&q={query}"
    

class URLs1337x:
    BASE = "https://www.1377x.to"
    SEARCH = BASE + "/search/{query}/{page}/"
    TORRENT = BASE + "/torrent/{id}/d"