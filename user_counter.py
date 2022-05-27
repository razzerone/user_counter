import json
import sys

import requests
from requests import HTTPError

from database.user_repository import UserRepository
from database.visit_repository import VisitsRepository


class UserCounter:
    """Класс, внутри которого реализуются необходимые для реализации счетчика посещений функции."""

    def __init__(self, visit_repository: VisitsRepository,
                 user_repository: UserRepository):
        self._visit_repo = visit_repository
        self._user_repo = user_repository

    def add_visitor(self, ip: str, page: str, user_agent: str,
                    user_id: int | None) -> int:
        """Функция, которая обращается к репозиторию для добавления пользователя в базу данных."""
        country = self.get_ip_country(ip)

        return self._visit_repo.add_new_visit(ip, page, user_agent, country,
                                              user_id)

    @staticmethod
    def get_ip_country(ip: str):
        """Функция, определяющая страну, из которой было выполнено посещение, по входному IP-адресу."""
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
        except (ConnectionError, HTTPError):
            return '*'

        content = json.loads(response.content)

        try:
            return content['country']
        except Exception as e:
            return '*'
