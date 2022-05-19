import sqlite3

from repository import Repository


class SQLiteRepository(Repository):
    def __init__(self):
        with sqlite3.connect('data.db') as connection:
            with open('setup.sql') as f:
                connection.executescript(f.read())
                connection.commit()

    def _remove_old_lines(self):
        pass

    def add_new_user(self, ip: str, page: str, user_agent: str, country: str):
        with sqlite3.connect('data.db') as con:
            con.execute(
                'INSERT INTO users (ip, page, user_agent, country) '
                'VALUES (?, ?, ?, ?) ',
                (ip, page, user_agent, country)
            )
            con.commit()

    def get_users_count(self):
        with sqlite3.connect('data.db') as connection:
            count = connection.execute(
                'SELECT COUNT(*) FROM users'
            ).fetchone()
            connection.commit()

        return count

    def get_last(self):
        with sqlite3.connect('data.db') as connection:
            last = connection.execute(
                'SELECT id, created, ip, page, user_agent, country FROM users '
                'WHERE (id = (SELECT MAX(id) FROM users))'
            ).fetchone()
            connection.commit()

        return last

    def get_all_users(self):
        with sqlite3.connect('data.db') as connection:
            last = connection.execute(
                'SELECT * FROM users '
            ).fetchall()
            connection.commit()

        return last
