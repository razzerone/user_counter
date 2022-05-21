from datetime import timedelta
from flask import Flask, request, jsonify, session, render_template, Blueprint
from flask_login import login_required, login_manager, UserMixin, LoginManager
from peewee import Model, CharField, DateTimeField, SqliteDatabase
from werkzeug.security import generate_password_hash, check_password_hash

import SQLite_impl
from smart_repo import SmartRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = 'qwertyyaebusobak'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = SmartRepo()
user_counter = UserCounter(repo)
db = SqliteDatabase('data.db')
login_manager = LoginManager(app)
login_manager.login_view = 'login'


@app.route('/')
@login_required
def counter():
    if 'visited' not in session:
        session['visited'] = True
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string
        )

    return render_template("layout.html")


@app.route('/login', methods=['post',  'get'])
def login():
    message = ''
    if request.method == 'POST':
        print(request.form)
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'root' and password == 'pass':
        message = "Correct username and password"
    else:
        message = "Wrong username or password"

    return render_template('login.html', message=message)

@app.route('/signup')
def signup():
    return "aaaa"


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


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)


@login_manager.user_loader
class User(Model, UserMixin):
    name = CharField()
    password_hash = CharField()
    email = CharField()
    created_on = DateTimeField()
    updated_on = DateTimeField()

    class Meta:
        database = db

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


if __name__ == '__main__':
    app.run()
