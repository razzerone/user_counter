import datetime

from DataLine import DataLine
from repository import Repository


class SmartRepo(Repository):
    def __init__(self):
        self.repo = DataLine
        '''it did not work yet,but I am trying.....'''
        self.repo.delete().where(self.repo.date.between(
            datetime.date.today(),
            datetime.date.today() + datetime.timedelta(seconds=20)))
        self.repo.create_table()

    def add_new_user(self, ip: str, page: str, user_agent: str, country: str):
        a = self.repo(ip=ip, page=page, user_agent=user_agent, country=country,
                      date=datetime.datetime.now().strftime("%H:%M:%S"))
        a.save()

    def get_last(self):
        return DataLine.select().order_by(DataLine.id.desc()).tuples()[-1]

    def get_users_count(self):
        return DataLine.select().order_by(DataLine.id.desc()).get()
