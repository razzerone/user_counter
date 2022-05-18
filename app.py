from datetime import timedelta

from flask import Flask, request, jsonify, session

from repository import Repository
from stupid_repo import StupidRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = 'qwertyyaebusobak'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = StupidRepo()
user_counter = UserCounter(repo)


@app.route('/')
def hello_world():
    if 'visited' not in session:
        session['visited'] = True
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string
        )

    return jsonify(repo.get_users())


if __name__ == '__main__':
    app.run()
