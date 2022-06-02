import dataclasses


@dataclasses.dataclass
class Visit:
    id: int
    ip: str
    page: int
    time: int
    user_agent: str
    browser: str
    os: str
    country: str
    user_id: int | None
