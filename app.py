from flask import request, session, render_template
from flask_login import login_required, UserMixin, login_user

from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager
from peewee import SqliteDatabase

from database.UserRepository_SqlAlchemy import UsersRepo
from smart_repo import SmartRepo
from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = secrets.token_bytes()

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = SmartRepo()
user_counter = UserCounter(repo)
user_repo = UsersRepo()
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


@app.route('/login', methods=['post', 'get'])
def login():
    message = ''
    if request.method == 'POST':
        print(request.form)
        username = request.form.get('username')
        password = request.form.get('password')

        i, login_, password_ = user_repo.get_user_by_login(username)

        if check_password_hash(password_, password):
            login_user(User(i, username, password))
            message = 'login succesful'
        else:
            message = "login unsuccessful"

    return render_template('login.html', message=message)


@app.route('/signup')
def signup():
    return render_template('signup.html')


@app.route('/validate_reg', methods=['GET', 'POST'])
def validate():
    name = request.form.get('name')
    password = request.form.get('password')
    if user_repo.get_user_by_login(name) is not None:
        return render_template('signup.html', message="пользователь существует")
    user_repo.add_new_user(name, password)
    return render_template('signup.html', message="пользователь зарегистрирован")


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
class User(UserMixin):
    def __init__(self, id, login, password, active=True):
        self.id = id
        self.password_hash = password
        self.login = login
        self.active = active

    def is_active(self):
        # Here you should write whatever the code is
        # that checks the database if your user is active
        return self.active

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True

    def get_id(self):
        return (self.id)


@login_manager.user_loader
def load_user(id):
    # 1. Fetch against the database a user by `id`
    # 2. Create a new object of `User` class and return it.
    _, login, hash = user_repo.get_user_by_id(id)
    return User(id, login, hash)


if __name__ == '__main__':
    app.run()
