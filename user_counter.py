import json
import requests

from peewee import *

from repository import Repository
from DataLine import DataLine


class UserCounter:
    def __init__(self, user_repository: Repository):
        self._user_repo = user_repository

    def add_visitor(self, ip: str, page: str, user_agent: str):
        country = self.get_ip_country(ip)
        self._user_repo.add_new_user(ip, page, user_agent, country)

    @staticmethod
    def get_ip_country(ip: str):

        response = requests.get(f"https://ipinfo.io/{ip}/json")

        content = json.loads(response.content)

        try:
            return content['country']
        except Exception as e:
            return '*'
