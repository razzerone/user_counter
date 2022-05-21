class UserRepository:
    def add_new_user(self, login, password):
        raise NotImplementedError

    def get_user_by_id(self, id):
        raise NotImplementedError

    def get_user_by_login(self, login):
        raise NotImplementedError
