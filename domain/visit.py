import dataclasses


@dataclasses.dataclass
class Visit:
    id: int
    ip: str
    page: int
    time: str
    user_agent: str
    browser: str
    os: str
    country: str
    user_id: int | None


def convert_date(date: str) -> str:
    return (f'{date[6:8]}-{date[4:6]}-{date[0:4]} '
            f'{date[8:10]}:{date[10:12]}:{date[12:14]}')
