import json
import sys

import requests
from requests import HTTPError

from repository import Repository


class UserCounter:
    def __init__(self, user_repository: Repository):
        self._user_repo = user_repository

    def add_visitor(self, ip: str, page: str, user_agent: str):
        country = self.get_ip_country(ip)
        self._user_repo.add_new_user(ip, page, user_agent, country)

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
