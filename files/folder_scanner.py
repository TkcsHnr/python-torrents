import os
from dataclasses import dataclass
import magic


@dataclass
class FolderContents:
    video_files: list[str]
    subfolders: list[str]


class FolderScanner:

    def __init__(self) -> None:
        self._mime = magic.Magic()

    def get_folder_contents(self, path: str) -> FolderContents:
        try:
            items = os.listdir(path)

            subfolders = []
            video_files = []

            for item in items:
                item_path = os.path.join(path, item)

                if os.path.isdir(item_path):
                    subfolders.append(item)

                elif self._mime.from_file(item_path).startswith('video'):
                    video_files.append(item)

            return FolderContents(video_files, subfolders)
        except FileNotFoundError:
            print(f"The given path '{path}' does not exist.")
            return FolderContents([], [])
