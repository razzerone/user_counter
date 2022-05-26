from flask import request, session, render_template, redirect, url_for
from flask_login import login_required, UserMixin, login_user, current_user, logout_user

from werkzeug.security import check_password_hash
import secrets
from datetime import timedelta

from flask import Flask
from flask_login import LoginManager

from database.user_repository_sqlalchemy import UsersRepositoryImpl
from database.visit_repository_sqlalchemy import VisitsRepositoryImpl

from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = secrets.token_bytes()

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

repo = VisitsRepositoryImpl()
user_repo = UsersRepositoryImpl()
user_counter = UserCounter(repo, user_repo)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.route('/')
def counter():
    """Функция, отвечающая за отображение главной страницы."""
    return render_template("mainpage.html")


@app.errorhandler(404)
def page_not_found():
    """Функция, отвечающая за отображение любой несуществующей страницы."""
    return render_template('404.html'), 404


@app.route('/auth')
@login_required
def auth():
    """Функция, отвечающая за страницу,открывающуюся после выполнения входа."""
    return render_template("layout.html")


@app.route('/anon')
def anon():
    """
    Функция, отвечающая за страницу, открывающуюся для пользователей, пожелавших остаться анонимными.


    Внутри так же происходит обработка посещения - если в данной сессии пользователь уже
    посещал страницу, то его посещение можно не считать.
    """
    if 'visited' not in session:
        session['visited'] = True
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string,
            None
        )
    return render_template("layoutforanonymo.html")


@app.route('/login', methods=['post', 'get'])
def login():
    """
    Функция, отвечающая за страницу, открывающуюся для пользователей, пожелавших остаться анонимными.


    Внутри  происходит обработка вводимых данных - проверяются логин и пароль.Если они есть в базе данных,
    то выполняется вход и посещение заносится в базу данных.
    """
    if current_user.is_authenticated:
        return render_template('login_for_authenticated.html')
    message = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        a = user_repo.get_user_by_login(username)
        if a is None:
            message = "User does not exist"
        else:
            i, login_, password_ = a
            if check_password_hash(password_, password):
                session['id'] = i
                login_user(User(i, username, password))
                user_counter.add_visitor(
                    request.remote_addr,
                    request.path,
                    request.user_agent.string,
                    session['id']
                )
                return redirect(url_for('auth'))
            else:
                message = "Login failed"

    return render_template('login.html', message=message)


@app.route('/signup')
def signup():
    """Функция, отвечающая за отображение страницы регистрации пользователя."""
    return render_template('signup.html')


@app.route('/validate_reg', methods=['GET', 'POST'])
def validate():
    """Функция, отвечающая за валидацию регистрируемого пользователя."""
    name = request.form.get('name')
    password = request.form.get('password')
    if user_repo.get_user_by_login(name) is not None:
        return render_template('signup.html', message="User already exists")
    user_repo.add_new_user(name, password)
    return render_template('signup.html', message="User has been registered")


@app.route('/last')
def last_user():
    """Функция, отвечающая за отображение страницы, показывающей последнюю запись о входе."""
    return render_template("last_second.html", line=repo.get_last())


@app.route("/logout")
def logout():
    """Функция, отвечающая за выход пользователя и отображение главной страницы. """
    logout_user()
    return render_template("mainpage.html")


@app.route('/first')
def first_user():
    """Функция, отвечающая за отображение страницы, показывающей первую запись о входе."""
    return render_template("last_second.html", line=repo.get_first())


@app.route('/count')
def count():
    """Функция, отвечающая за отображение страницы, показывающей количество посещений сайта."""
    return render_template("for_counter.html", counter=repo.get_users_count())


@app.route('/all')
def all_users():
    """Функция, отвечающая за отображение страницы, показывающей все посещения сайта."""
    users = [user for user in repo.get_all_records()]

    return render_template("view.html", table=users)


@app.route('/profile')
def profile():
    """Функция, отвечающая за отображение страницы, показывающей все посещения сайта конкретным пользователем."""
    aaa = list(repo.get_records_by_id(session['id']))

    return render_template("view.html", table=aaa)


@login_manager.user_loader
def load_user(id_):
    """Функция, возвращающая пользователя, соотвествующего входному идентификатору."""
    ids, login, psw = user_repo.get_user_by_id(int(id_))
    return User(ids, psw, login)


class User(UserMixin):
    """Модель, необходимая Flask для хранения данных о пользователе."""
    def __init__(self, id, login, password, active=True):
        self.id = id
        self.password_hash = password
        self.login = login
        self.active = active


if __name__ == '__main__':
    app.run()
