from dotenv import load_dotenv, set_key
import os

ENV_PATH = "files/.env"
DEFAULT_SAVEPATH_KEY = "default_savepath"

WATCHED_PATHS_FILE = "files/paths.dat"


class PathManager:

    def __init__(self) -> None:
        load_dotenv(dotenv_path=ENV_PATH)

    def _get_default_videos_folder(self) -> str:
        user_home = os.path.expanduser("~")
        videos_path = os.path.join(user_home, "Videos")
        return videos_path

    def _get_env(self, key: str):
        if key in os.environ.keys():
            return os.environ[key]

        return None

    def set_default_save_path(self, default_save_path: str):
        os.environ[DEFAULT_SAVEPATH_KEY] = default_save_path
        set_key(ENV_PATH, DEFAULT_SAVEPATH_KEY, default_save_path)

    def get_default_savepath(self) -> str:
        default_savepath = self._get_env(DEFAULT_SAVEPATH_KEY)

        if default_savepath:
            return default_savepath

        videos_folder = self._get_default_videos_folder()
        self.set_default_save_path(videos_folder)
        return videos_folder

    def add_watch_path(self, path: str):
        with open(WATCHED_PATHS_FILE, mode="a") as dat_file:
            dat_file.write(path + '\n')

    def get_watched_paths(self) -> list[str]:
        paths = []
        with open(WATCHED_PATHS_FILE, mode="r") as dat_file:
            for line in dat_file.readlines():
                paths.append(line.strip())
        return paths

    def remove_watch_path(self, path: str):
        with open(WATCHED_PATHS_FILE, mode="r") as dat_file:
            lines = dat_file.readlines()

        lines = [line for line in lines if line.strip() != path]

        with open(WATCHED_PATHS_FILE, mode="w") as dat_file:
            dat_file.writelines(lines)
