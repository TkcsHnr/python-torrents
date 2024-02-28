from dotenv import load_dotenv, set_key
import os
from dataclasses import dataclass
from clients import ClientName


@dataclass
class ClientCredentials:
    username: str
    password: str

    def missing(self) -> bool:
        return self.username is None or self.password is None


@dataclass
class QBitTorrentCredentials:
    host: str
    port: int
    username: str
    password: str

    def missing(self) -> bool:
        return self.host is None or self.port is None or self.username is None or self.password is None


class CredentialsManager:

    def __init__(self) -> None:
        load_dotenv()
        self._qbittorrent_host_key = 'qbittorrent_host'
        self._qbittorrent_port_key = 'qbittorrent_port'
        self._qbittorrent_username_key = 'qbittorrent_username'
        self._qbittorrent_password_key = 'qbittorrent_password'

    def _get_env(self, key: str):
        if key in os.environ.keys():
            return os.environ[key]

        return None

    def get_client_credentials(self, name_prefix: ClientName) -> ClientCredentials:
        username_key = name_prefix.value + '_username'
        password_key = name_prefix.value + '_password'

        username = self._get_env(username_key)
        password = self._get_env(password_key)

        return ClientCredentials(username, password)

    def set_client_credentials(self, name_prefix: ClientName, username: str, password: str):
        username_key = name_prefix.value + '_username'
        password_key = name_prefix.value + '_password'

        if username:
            os.environ[username_key] = username
            set_key('.env', username_key, username)
        if password:
            os.environ[password_key] = password
            set_key('.env', password_key, password)

    def get_qbittorrent_credentials(self) -> QBitTorrentCredentials:
        host = self._get_env(self._qbittorrent_host_key)
        port = self._get_env(self._qbittorrent_port_key)
        username = self._get_env(self._qbittorrent_username_key)
        password = self._get_env(self._qbittorrent_password_key)

        return QBitTorrentCredentials(host, port, username, password)

    def set_qbittorrent_credentials(self, host: str, port: int, username: str, password: str):
        if host:
            os.environ[self._qbittorrent_host_key] = host
            set_key('.env', self._qbittorrent_host_key, host)
        if port:
            os.environ[self._qbittorrent_port_key] = port
            set_key('.env', self._qbittorrent_port_key, port)
        if username:
            set_key('.env', self._qbittorrent_username_key, username)
            os.environ[self._qbittorrent_username_key] = username
        if password:
            os.environ[self._qbittorrent_password_key] = password
            set_key('.env', self._qbittorrent_password_key, password)
