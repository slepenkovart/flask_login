import datetime
from sextest import DataBase
from hashlib import md5
from flask import request, make_response, redirect


class UserLogin:
    def __init__(self):
        self.db = DataBase()

    def _encrypt_password(self, password: str) -> str:
        encrypted = md5(password.encode('utf-8')).hexdigest()
        return encrypted

    def is_authenticated(self):
        return True

    def login_required(self, func):
        def inner(*args, **kwargs):
            if not request.cookies.get('session'):
                return "loqin required <a href='/reg'>REG</a>"
            else:
                if not request.cookies.get('login'):
                    return "loqin required <a href='/reg'>REG</a>"
                else:
                    user = self.db.get_user(request.cookies.get('login'))
                    if user is None:
                        return "pizdabol!!!"
                    last = user['last_activity'].split('.')[0]
                    last = datetime.datetime.strptime(last, "%Y-%m-%d %H:%M:%S")
                    now = datetime.datetime.now()
                    delta = (now - last).total_seconds() / 60
                    self.db.update_activity(user)

                    if delta > 15:
                        res = make_response("update login")
                        res.delete_cookie('session')
                        res.delete_cookie('login')
                        return res
                    return func(*args, **kwargs)
        inner.__name__=func.__name__
        return inner

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.__user['id'])


class User:
    def __init__(self, user_id, login, password, session, last_activity) -> None:
        self.user_id = user_id
        self.login = login
        self.password = password
        self.session = session
        self.last_activity = last_activity
