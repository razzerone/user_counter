import sqlalchemy.exc
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

from database.tables import engine
from database.tables import DatabaseUser
from database.user_repository import UserRepository


class UsersRepositoryImpl(UserRepository):
    """Данный класс является реализацией UserRepository,которая работает,опираясь на SqlAlchemy."""
    def __init__(self):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    """Реализация добавления пользователя в базу данных."""
    def add_new_user(self, login, password) -> int:
        session = self.session_factory()
        user = DatabaseUser(login=login, password_hash=generate_password_hash(password))
        session.add(user)
        session.commit()

        return user.id

    """Реализация получения пользователя по идентификатору."""
    def get_user_by_id(self, id_: int) -> tuple[int, str, str] | None:
        session = self.session_factory()
        try:
            user = session.query(DatabaseUser).filter(DatabaseUser.id == id_).one()
            session.commit()

            return id_, user.login, user.password_hash
        except sqlalchemy.exc.NoResultFound:
            return None

    """Реализация получения пользователя по логину."""
    def get_user_by_login(self, login):
        session = self.session_factory()

        try:
            user = session.query(DatabaseUser).filter(DatabaseUser.login == login).one()
            session.commit()

            return user.id, login, user.password_hash
        except sqlalchemy.exc.NoResultFound:
            return None
