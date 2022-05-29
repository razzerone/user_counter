from datetime import datetime
from typing import Any

from domain.visit import Visit

import setting


class VisitsRepository:
    """Данный класс является прослойкой между работой базы данных и работой самого приложения,необходимы для операций
        с записями. """
    def add_new_visit(self, ip: str, page: str, user_agent: str, country: str, user_id: int) -> int:
        """Функция позволяет обратиться к базе данных и добавить в нее запись."""
        raise NotImplementedError

    def get_last(self) -> tuple[Any, Any, Any, Any, Any, Any, Any]:
        """Функция позволяет обратиться к базе данных и получить из нее последнюю запись."""
        raise NotImplementedError

    def get_users_count(self) -> int:
        """Функция позволяет обратиться к базе данных и получить из нее количество записей."""
        raise NotImplementedError

    @staticmethod
    def get_current_timestamp() -> str:
        """Функция, необходимая для форматирования времени"""
        return datetime.now().strftime(setting.database_datetime_format)
