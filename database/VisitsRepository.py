from datetime import datetime
from typing import Any

from Domain.Visit import Visit

import setting


class VisitsRepository:
    def add_new_visit(self, ip: str, page: str, user_agent: str, country: str, user_id: int) -> int:
        raise NotImplementedError

    def get_last(self) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
        raise NotImplementedError

    def get_users_count(self) -> int:
        raise NotImplementedError

    @staticmethod
    def get_current_timestamp() -> str:
        return datetime.now().strftime(setting.datetime_format)
