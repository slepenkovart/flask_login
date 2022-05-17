import datetime
from DB import DataBase
from hashlib import md5
from flask import request, make_response, redirect, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class UserLogin:
    def __init__(self):
        self.db = DataBase()
        self.auth_redirect = '/home'
        self.main_page = '/'
        self.login_page='/login'

    def reg(self, login, password):
        password = self._encrypt_password(password)
        user = self.db.add_user(login, password)
        res = make_response(redirect('/home'))
        res.set_cookie('session', user['session'], max_age=60 * 60 * 24 * 365 * 2)
        res.set_cookie('login', user['login'], max_age=60 * 60 * 24 * 365 * 2)
        return res

    def auth(self, login, password):
        user = self.db.get_user(login)
        if user is None:
            return 'KTO TI'
        if user['password'] == self._encrypt_password(password):
            res = make_response(redirect(self.auth_redirect))
            self.db.update_activity('login')
            res.set_cookie('session', user['session'], max_age=60 * 60 * 24 * 365 * 2)
            res.set_cookie('login', login, max_age=60 * 60 * 24 * 365 * 2)
            return res

    def _encrypt_password(self, password: str) -> str:
        encrypted = md5(password.encode('utf-8')).hexdigest()
        return encrypted

    def is_authenticated(self):
        return True

    def login_required(self, func):
        def inner(*args, **kwargs):
            if not request.cookies.get('session'):
                msg = "You are not authorized!"
                return render_template("401.html", message=msg,redirect_url=self.login_page), 401
                # return "loqin required <a href='/reg'>REG</a>"
            else:
                if not request.cookies.get('login'):
                    msg = "You are not authorized!"
                    return render_template("401.html", message=msg,redirect_url=self.login_page), 401
                else:
                    user = self.db.get_user(request.cookies.get('login'))
                    if user is None:
                        msg = "Bad authorized data in your cookies!"
                        res = make_response(render_template("401.html", message=msg,redirect_url=self.login_page))
                        res.delete_cookie("login")
                        res.delete_cookie("session")
                        return res,401
                    last = user['last_activity'].split('.')[0]
                    last = datetime.datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
                    now = datetime.datetime.now()
                    delta = (now - last).total_seconds() / 60
                    print(user)
                    self.db.update_activity(user['login'])

                    if delta > 15:
                        self.db.update_session(user['login'])
                        res = make_response("update login")
                        res.delete_cookie('session')
                        res.delete_cookie('login')
                        return res
                    return func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner

    def logout(self):
        login = request.cookies.get("login")
        res = make_response(redirect(self.main_page))
        res.delete_cookie('session')
        res.delete_cookie('login')
        return res

    def _check_user(self, login, session):
        user = self.db.get_user(login)
        if user is not None:
            if user['session'] == session:
                return True
            else:
                return False
        return False

    def is_active(self):
        return True

    def is_anonymous(self, func):
        def inner(*args, **kwargs):
            login=request.cookies.get('login')
            session=request.cookies.get('session')
            if login and session:
                if self._check_user(login,session):
                    return redirect(self.auth_redirect)
                else:
                    res = make_response(redirect(self.main_page))
                    res.delete_cookie('session')
                    res.delete_cookie('login')
                    return res
            else:
                return func(*args, **kwargs)

        inner.__name__ = func.__name__
        return inner


class User:
    def __init__(self, user_id, login, password, session, last_activity) -> None:
        self.user_id = user_id
        self.login = login
        self.password = password
        self.session = session
        self.last_activity = last_activity


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    repeat_password = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
