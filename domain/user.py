import dataclasses


@dataclasses.dataclass
class User:
    id: int
    login: str
    password_hash: str
