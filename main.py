from flask import Flask, request, make_response, url_for, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from login_manager import UserLogin, LoginForm, RegForm
import logging

app = Flask(__name__)
user_login = UserLogin()

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite////C:/Users/Artem/Desktop/logins.db'
app.config['SECRET_KEY'] = 'thisissecret'


#
# db=SQLAlchemy(app)


@app.route('/')
def start():
    return render_template("index.html", title="Главная страница")


@app.route('/reg', methods=['GET', 'POST'])
@user_login.is_anonymous
def reg():
    form = RegForm()
    print('da')
    if form.validate_on_submit():
        print(form.repeat_password.data,form.password.data)
        if form.repeat_password.data == form.password.data:
            print("vse ok")
            return user_login.reg(form.username.data, form.password.data)
        else:
            print("dont sovpadayut")
            return render_template('reg.html', title='Sign up', form=form, bad_pass=True)
    return render_template('reg.html', title='Sign up', form=form)


@app.route('/home')
@user_login.login_required
def home():
    return render_template("home.html")
    return f"you are at home, dear {request.cookies.get('login')}"


@app.route('/login', methods=['GET', 'POST'])
@user_login.is_anonymous
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return user_login.auth(form.username.data, form.password.data)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
@user_login.login_required
def logout_user():
    return user_login.logout()





if __name__ == '__main__':
    app.run()
