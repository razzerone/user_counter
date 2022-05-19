from peewee import *

db = SqliteDatabase('data.db')


class DataLine(Model):
    ip = CharField()
    page = CharField()
    user_agent = CharField()
    country = CharField()
    date= DateTimeField()

    class Meta:
        database = db
