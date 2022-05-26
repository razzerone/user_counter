import json
import sys

import requests
from requests import HTTPError

from database.UserRepository import UserRepository
from database.VisitsRepository import VisitsRepository
from repository import Repository


class UserCounter:
    def __init__(self, visit_repository: VisitsRepository, user_repository: UserRepository):
        self._visit_repo = visit_repository
        self._user_repo = user_repository

    def add_visitor(self, ip: str, page: str, user_agent: str, user_id: int | None) -> int:
        country = self.get_ip_country(ip)

        return self._visit_repo.add_new_visit(ip, page, user_agent, country, user_id)

    @staticmethod
    def get_ip_country(ip: str):
        try:
            response = requests.get(f"https://ipinfo.io/{ip}/json")
        except ConnectionError as e:
            print('Проблемы при соединении с сетью')
            sys.exit(-1)
        except HTTPError as e:
            return '*'

        content = json.loads(response.content)

        try:
            return content['country']
        except Exception as e:
            return '*'
