from flask import Flask, request, make_response, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from login_manager import UserLogin

app = Flask(__name__)
user_login = UserLogin()


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite////C:/Users/Artem/Desktop/logins.db'
# app.config['SECRET_KEY'] = 'thisissecret'
#
# db=SQLAlchemy(app)


@app.route('/')
@user_login.login_required
def start():
    return 'da'


@app.route('/reg')
def reg():
    res = make_response("Setting a cookie")
    res.set_cookie('session', 'b7d4ab1927e5363ac5587ebba2721955', max_age=60 * 60 * 24 * 365 * 2)
    res.set_cookie('login', 'qwe', max_age=60 * 60 * 24 * 365 * 2)
    return res


@app.route('/auth')
def auth():
    res = make_response("Wait a minute, we are logging")
    res.set_cookie('session', 'b7d4ab1927e5363ac5587ebba2721955', max_age=60 * 60 * 24 * 365 * 2)
    res.set_cookie('login', 'qwe', max_age=60 * 60 * 24 * 365 * 2)
    return res

@app.route('/home')
@user_login.login_required
def home():
    return "yoa are at home"



if __name__ == '__main__':
    app.run()
