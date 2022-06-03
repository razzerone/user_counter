from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash

import domain.user
from database.tables import DatabaseUser
from database.user_repository import UserRepository


class UsersRepositoryImpl(UserRepository):
    """
    Данный класс является реализацией UserRepository, которая работает,
    опираясь на SqlAlchemy.
    """

    def __init__(self, engine=None):
        self.engine = engine
        self.session_factory = sessionmaker(bind=engine)

    def add_new_user(self, login, password) -> int:
        """Реализация добавления пользователя в базу данных."""
        with self.session_factory() as session:
            user = DatabaseUser(login=login,
                                password_hash=generate_password_hash(password))
            session.add(user)
            session.commit()

            return user.id

    def get_user_by_id(self, id_: int) -> domain.user.User | None:
        """Реализация получения пользователя по идентификатору."""
        with self.session_factory() as session:
            user = session.query(DatabaseUser).filter(
                DatabaseUser.id == id_).one_or_none()
            session.commit()

            if user is None:
                return None

            return domain.user.User(
                id=id_,
                login=user.login,
                password_hash=user.password_hash
            )

    def get_user_by_login(self, login):
        """Реализация получения пользователя по логину."""
        with self.session_factory() as session:
            user = session.query(DatabaseUser).filter(
                DatabaseUser.login == login).first()
            session.commit()

            if user is None:
                return None

            return domain.user.User(
                id=user.id,
                login=login,
                password_hash=user.password_hash
            )
