from dotenv import load_dotenv, set_key
import os
from dataclasses import dataclass
from clients import ClientName


ENV_PATH = "credentials/.env"

QBITTORRENT_HOST_KEY = 'qbittorrent_host'
QBITTORRENT_PORT_KEY = 'qbittorrent_port'
QBITTORRENT_USERNAME_KEY = 'qbittorrent_username'
QBITTORRENT_PASSWORD_KEY = 'qbittorrent_password'


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
        load_dotenv(dotenv_path=ENV_PATH)

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
            set_key(ENV_PATH, username_key, username)
        if password:
            os.environ[password_key] = password
            set_key(ENV_PATH, password_key, password)

    def get_qbittorrent_credentials(self) -> QBitTorrentCredentials:
        host = self._get_env(QBITTORRENT_HOST_KEY)
        port = self._get_env(QBITTORRENT_PORT_KEY)
        username = self._get_env(QBITTORRENT_USERNAME_KEY)
        password = self._get_env(QBITTORRENT_PASSWORD_KEY)

        return QBitTorrentCredentials(host, port, username, password)

    def set_qbittorrent_credentials(self, host: str, port: int, username: str, password: str):
        if host:
            os.environ[QBITTORRENT_HOST_KEY] = host
            set_key(ENV_PATH, QBITTORRENT_HOST_KEY, host)
        if port:
            os.environ[QBITTORRENT_PORT_KEY] = port
            set_key(ENV_PATH, QBITTORRENT_PORT_KEY, port)
        if username:
            set_key(ENV_PATH, QBITTORRENT_USERNAME_KEY, username)
            os.environ[QBITTORRENT_USERNAME_KEY] = username
        if password:
            os.environ[QBITTORRENT_PASSWORD_KEY] = password
            set_key(ENV_PATH, QBITTORRENT_PASSWORD_KEY, password)
