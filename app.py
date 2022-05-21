from datetime import timedelta
from flask import Flask, request, jsonify, session, render_template, Blueprint
from flask_login import login_required
import SQLite_impl
from smart_repo import SmartRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = 'qwertyyaebusobak'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = SmartRepo()
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

    return render_template("layout.html")


@app.route('/login')
def login():
    return 'Login'


@app.route('/last')
def last_user():
    return str(repo.get_last())


@app.route('/first')
def first_user():
    return str(repo.get_first())


@app.route('/count')
def count():
    return str(repo.get_users_count())


@app.route('/all')
def all_users():
    users = [user for user in repo.get_all_users()]

    return render_template("view.html", list=users)


@app.route('/profile')
def aaaa():
    return "aaa"


if __name__ == '__main__':
    app.run()
