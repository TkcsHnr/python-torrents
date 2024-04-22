class Torrent:
    def __init__(self, id: int, title: str, size: str, seed: int, leech: int, download: str = None, magnet: str = None):
        self.id = id
        self.title = title
        self.size = size
        self.seed = seed
        self.leech = leech
        self.download = download
        self.magnet = magnet
        
    def __str__(self) -> str:
        return str({
            "id": self.id,
            "title": self.title,
            "size": self.size,
            "seed": self.seed,
            "leech": self.leech,
            "download": self.download,
            "magnet": self.magnet
        })