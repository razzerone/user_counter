from peewee import *

db = SqliteDatabase('data.db')


class DataLine(Model):
    ip = CharField()
    page = CharField()
    user_agent = CharField()
    country = CharField()

    class Meta:
        database = db


