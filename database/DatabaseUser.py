from flask_login import UserMixin
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash



engine = create_engine('sqlite:///database.db', echo=True)
Base = declarative_base()


class DatabaseUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)

    def __repr__(self):
        return f'<User(id={self.id},login={self.login})>'

    # def set_password(self, password):
    #     self.password_hash = generate_password_hash(password)
    #
    # def check_password(self, password):
    #     return check_password_hash(self.password_hash, password)
