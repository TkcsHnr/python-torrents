class Torrent:
    def __init__(self, id: int, title: str, size: str, seed: int, leech: int, download: str):
        self.id = id
        self.title = title
        self.size = size
        self.seed = seed
        self.leech = leech
        self.download = download