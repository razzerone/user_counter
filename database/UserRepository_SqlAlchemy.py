import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from database.tables import engine
from database.tables import DatabaseUser
from database.UserRepository import UserRepository


class UsersRepositoryImpl(UserRepository):
    def __init__(self):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def add_new_user(self, login, password) -> int:
        session = self.session_factory()
        user = DatabaseUser(login=login, password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()

        return user.id

    def get_user_by_id(self, id_: int) -> tuple[int, str, str] | None:
        session = self.session_factory()
        try:
            user = session.query(DatabaseUser).filter(DatabaseUser.id == id_).one()
            session.commit()

            return id_, user.login, user.password_hash
        except sqlalchemy.exc.NoResultFound:
            return None

    def get_user_by_login(self, login):
        session = self.session_factory()

        try:
            user = session.query(DatabaseUser).filter(DatabaseUser.login == login).one()
            session.commit()

            return user.id, login, user.password_hash
        except sqlalchemy.exc.NoResultFound:
            return None
