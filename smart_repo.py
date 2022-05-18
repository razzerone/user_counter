from DataLine import DataLine
from repository import Repository


class SmartRepo(Repository):
    def __init__(self):
        self.repo = DataLine
        self.repo.create_table()

    def add_new_user(self, ip: str, page: str, user_agent: str, country: str):
        a = self.repo(ip=ip,page=page,user_agent=user_agent,country=country)
        a.save()

    def get_users(self):
        return self.repo

    def get_users_count(self):
        return DataLine.select().count()
