from dataclasses import dataclass

@dataclass
class RunData:
    id: str
    weblink: str
    game: str
    times: dict
    system: dict
    splits: dict
    values: dict
    links: list
    category: str
    videos: dict
    comment: str
    status: dict
    players: list
    level: str = None
    date: str = None
    submitted: str = None
    
