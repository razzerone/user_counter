from repository import Repository


class StupidRepo(Repository):
    def __init__(self):
        self.count = 0
        self.repo = dict()

    def add_new_user(self, ip: str, page: str, user_agent: str, country: str):
        self.repo[self.count] = {
            'ip': ip,
            'page': page,
            'user_agent': user_agent,
            'country': country
        }

        self.count += 1

    def get_last(self):
        return self.repo

    def get_users_count(self):
        return self.count
