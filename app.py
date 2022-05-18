from datetime import timedelta
from flask import Flask, request, jsonify, session

from smart_repo import SmartRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = 'qwertyyaebusobak'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = SmartRepo()
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
    return repo.get_users_count()


if __name__ == '__main__':
    app.run()
