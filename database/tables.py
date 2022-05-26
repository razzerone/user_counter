from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

import setting

engine = create_engine(setting.database, connect_args={'check_same_thread': False}, echo=setting.debug)
Base = declarative_base()


class DatabaseUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    login = Column(String)
    password_hash = Column(String)

    def __repr__(self):
        return f'<User(id={self.id},login={self.login})>'


class DatabaseVisit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    ip = Column(String)
    page = Column(String)
    time = Column(String)
    user_agent = Column(String)
    country = Column(String)
    user_id = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<Visit(id={self.user_id},ip={self.ip})>'
