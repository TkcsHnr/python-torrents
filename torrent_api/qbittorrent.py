import httpx
from utils import QBitTorrentURLs, QBitTorrentAuthError, ConnectionError
from credentials import QBitTorrentCredentials


class QBitTorrentClient:

    def __init__(self, host: str, port: int, username: str, password: str) -> None:
        self._url = f'http://{host}:{port}'
        self._SID = None
        self._username = username
        self._password = password

        self._login()
        
    @classmethod
    def from_credentials(cls, credentials: QBitTorrentCredentials):
        return cls(credentials.host, credentials.port, credentials.username, credentials.password)

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
            raise ConnectionError(
                "Error during qbittorrent login POST request") from e

    def download(self, url: str, savepath: str = None):
        if not self._SID:
            raise QBitTorrentAuthError(
                "SID for qbittorrent authentication not found")

        payload = {
            "urls": url,
            "savepath": savepath,
            "category": "python-movies"
        }
        cookies = {
            "SID": self._SID
        }

        try:
            httpx.post(
                self._url + QBitTorrentURLs.ADD, data=payload, cookies=cookies)
        except Exception as e:
            raise ConnectionError(
                "Error during qbittorrent download POST request") from e
