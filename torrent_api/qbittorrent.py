import httpx
from utils import QBitTorrentURLs, QBitTorrentAuthError


class QBitTorrentClient:

    def __init__(self, url: str, username: str, password: str, timeout: int = 1) -> None:
        self._url = url
        self._SID = None
        self._username = username
        self._password = password

        self._login()

    def _login(self):
        credentials = {
            "username": self._username,
            "password": self._password
        }
        try:
            response = httpx.post(
                self._url + QBitTorrentURLs.LOGIN, data=credentials)
            self._SID = response.cookies.get('SID')
        except Exception as e:
            print(e)

    def download(self, url: str, savepath: str = None):
        if not self._SID:
            raise QBitTorrentAuthError(
                "SID for qbittorrent authentication not found")

        payload = {
            "urls": url,
            "savepath": savepath
        }
        cookies = {
            "SID": self._SID
        }

        try:
            httpx.post(
                self._url + QBitTorrentURLs.ADD, data=payload, cookies=cookies)
        except Exception as e:
            print(e)
