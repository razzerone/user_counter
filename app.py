import os

import flask
import werkzeug
from flask import request, session, render_template, redirect, url_for, \
    send_from_directory
from flask_login import login_required, UserMixin, login_user, current_user, \
    logout_user

from werkzeug.security import check_password_hash
import secrets
from datetime import timedelta, datetime

from flask import Flask
from flask_login import LoginManager

import setting
from database import tables
from database.user_repository_sqlalchemy import UsersRepositoryImpl
from database.visit_repository_sqlalchemy import VisitsRepositoryImpl
from domain.messages import INVALID_PASSWORD, INVALID_USERNAME, \
    USER_ALREADY_EXISTS, USER_NOT_EXIST, USER_REGISTERED, INVALID_CREDENTIALS
from domain.names import ID, PASSWORD, USERNAME, VISITED

from user_counter import UserCounter

app = Flask(__name__)
app.secret_key = secrets.token_bytes()

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

visit_repo = VisitsRepositoryImpl(engine=tables.engine)
user_repo = UsersRepositoryImpl(engine=tables.engine)
user_counter = UserCounter(visit_repo, user_repo)

login_manager = LoginManager(app)
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before():
    flask.session.permanent = True


@app.route('/')
def counter():
    """Функция, отвечающая за отображение главной страницы."""
    if current_user.is_authenticated:
        return flask.redirect(url_for('auth'))
    return render_template("main_page.html")


@app.errorhandler(404)
def page_not_found(_):
    """Функция, отвечающая за отображение любой несуществующей страницы."""
    return render_template('404.html'), 404


@app.route('/auth')
@login_required
def auth():
    """
    Функция, отвечающая за страницу, открывающуюся после выполнения входа.
    """
    return render_template("layout.html")


@app.route('/anon')
def anon():
    """
    Функция, отвечающая за страницу, открывающуюся
    для пользователей, пожелавших остаться анонимными.

    Внутри так же происходит обработка посещения - если в данной сессии
    пользователь уже посещал страницу, то его посещение можно не считать.
    """
    if VISITED not in session:
        session[VISITED] = True
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string,
            None
        )
    return render_template("layout_anonymous.html")


def login_func(username, password):
    if username == '' and password == '':
        return render_template('login.html', message=INVALID_CREDENTIALS)
    if username == '':
        return render_template('login.html', message=INVALID_USERNAME)
    if password == '':
        return render_template('login.html', message=INVALID_PASSWORD)

    resp = user_repo.get_user_by_login(username)
    if resp is None:
        return render_template('login.html', message=USER_NOT_EXIST)

    id_, login_, password_ = resp.id, resp.login, resp.password_hash
    if check_password_hash(password_, password):
        session[ID] = id_
        login_user(User(id_, username, password))
        user_counter.add_visitor(
            request.remote_addr,
            request.path,
            request.user_agent.string,
            session[ID]
        )
        return redirect(url_for('auth'))
    return render_template('login.html', message='Login failed')


@app.route('/login', methods=['POST', 'GET'])
def login():
    """
    Функция, отвечающая за страницу, открывающуюся для пользователей,
    пожелавших остаться анонимными.
    Внутри происходит обработка вводимых данных - проверяются логин и пароль.
    Если они есть в базе данных, то выполняется вход и посещение заносится в
    базу данных.
    """
    if current_user.is_authenticated:
        return render_template('login_for_authenticated.html')

    if request.method == 'POST':
        username = request.form.get(USERNAME).strip()
        password = request.form.get(PASSWORD).strip()

        return login_func(username, password)

    return render_template('login.html', message='')


@app.route('/bydate')
def bydate():
    return render_template('recordsbydate.html')


@app.route('/recordsbydate', methods=['GET', 'POST'])
def showbydate():
    time=datetime.strptime(str(request.form.get('dateOne')),"%Y-%m-%d")\
        .strftime('%d-%m-%Y')


    table = visit_repo.get_records_by_date(str(time))
    return render_template('view.html', table=table)


@app.route('/signup')
def signup():
    """Функция, отвечающая за отображение страницы регистрации пользователя."""
    return render_template('signup.html')


@app.route('/validate_reg', methods=['GET', 'POST'])
def validate():
    """Функция, отвечающая за валидацию регистрируемого пользователя."""
    if request.form.get(USERNAME) is None \
            and request.form.get(PASSWORD) is None:
        return render_template('signup.html', message=INVALID_CREDENTIALS)
    if request.form.get(USERNAME) is None:
        return render_template('signup.html', message=INVALID_USERNAME)
    name = request.form.get(USERNAME).strip()
    if request.form.get(PASSWORD) is None:
        return render_template('signup.html', message=INVALID_PASSWORD)
    password = request.form.get(PASSWORD).strip()
    if user_repo.get_user_by_login(name) is not None:
        return render_template('signup.html', message=USER_ALREADY_EXISTS)
    user_repo.add_new_user(name, password)

    return login_func(name, password)

    # return render_template('s.html', message=USER_REGISTERED)


@app.route('/last')
def last_user():
    """
    Функция, отвечающая за отображение страницы, показывающей последнюю запись
    о входе.
    """
    return render_template(
        "last_second.html",
        line=visit_repo.get_last())


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico',
                               mimetype='image/vnd.microsoft.icon')


@app.route("/logout")
def logout():
    """
    Функция, отвечающая за выход пользователя и отображение главной страницы.
    """
    logout_user()
    return render_template("main_page.html")


@app.route('/first')
def first_user():
    """
    Функция, отвечающая за отображение страницы, показывающей первую запись о
    входе.
    """
    return render_template("last_second.html", line=visit_repo.get_first())


@app.route('/count')
def count():
    """
    Функция, отвечающая за отображение страницы, показывающей количество
    посещений сайта.
    """
    return render_template(
        "for_counter.html",
        counter=visit_repo.get_users_count()
    )


@app.route('/all')
def all_users():
    """
    Функция, отвечающая за отображение страницы, показывающей все посещения
    сайта.
    """
    return render_template(
        "view.html",
        table=visit_repo.get_all_records()
    )


@app.route('/profile')
@login_required
def profile():
    """
    Функция, отвечающая за отображение страницы, показывающей все посещения
    сайта конкретным пользователем.
    """
    return render_template(
        "view.html",
        table=visit_repo.get_records_by_id(session[ID])
    )


@login_manager.user_loader
def load_user(id_):
    """
    Функция, возвращающая пользователя, соответствующего входному
    идентификатору.
    """
    resp = user_repo.get_user_by_id(int(id_))
    return User(id_, resp.login, resp.password_hash)


class User(UserMixin):
    """Модель, необходимая Flask для хранения данных о пользователе."""

    def __init__(self, id_, login_, password, active=True):
        self.id = id_
        self.password_hash = password
        self.login = login_
        self.active = active


if __name__ == '__main__':
    app.run()
