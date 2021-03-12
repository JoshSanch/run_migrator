from dataclasses import dataclass

@dataclass
class RunData:
    id: str
    weblink: str
    game: str
    level: str = None
    category: str
    videos: dict
    comment: str
    status: dict
    players: list
    date: str = None
    submitted: str = None
    times: dict
    system: dict
    splits: dict
    values: dict
    links: list
