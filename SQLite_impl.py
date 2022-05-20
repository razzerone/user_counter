import re
import sqlite3

from repository import Repository


class SQLiteRepository(Repository):
    def __init__(self, db):
        self.db = db

        self.ip_re = re.compile(r'(\d{1,3}\.){3}\d{1,3}')

        with sqlite3.connect(self.db) as connection:
            with open('setup.sql') as f:
                connection.executescript(f.read())
                connection.commit()

    def _remove_old_lines(self):
        pass

    def add_new_user(self, ip: str, page: str, user_agent: str, country: str):
        if self.ip_re.fullmatch(ip) is None:
            raise IOError(f'invalid argument ip: {ip}')

        with sqlite3.connect(self.db) as con:
            con.execute(
                'INSERT INTO users (ip, page, user_agent, country) '
                'VALUES (?, ?, ?, ?) ',
                (ip, page, user_agent, country)
            )
            con.commit()

    def get_users_count(self):
        with sqlite3.connect(self.db) as connection:
            count = connection.execute(
                'SELECT COUNT(*) FROM users'
            ).fetchone()
            connection.commit()

        return count

    def get_last(self):
        with sqlite3.connect(self.db) as connection:
            last = connection.execute(
                'SELECT id, created, ip, page, user_agent, country FROM users '
                'WHERE (id = (SELECT MAX(id) FROM users))'
            ).fetchone()
            connection.commit()

        return last

    def get_all_users(self):
        with sqlite3.connect(self.db) as connection:
            last = connection.execute(
                'SELECT * FROM users '
            ).fetchall()
            connection.commit()

        return last
