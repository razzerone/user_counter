from datetime import timedelta
from flask import Flask, request, jsonify, session

import SQLite_impl
from smart_repo import SmartRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = 'qwertyyaebusobak'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = SQLite_impl.SQLiteRepository('data.db')
user_counter = UserCounter(repo)


@app.route('/')
def counter():
    if 'visited' not in session:
        session['visited'] = True
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string
        )

    repo.get_all_users()

    return str(repo.get_all_users())


@app.route('/last')
def all_users():
    return str(repo.get_last())


@app.route('/count')
def count():
    return str(repo.get_users_count())


if __name__ == '__main__':
    app.run()
