import sqlite3
from datetime import datetime
from hashlib import md5


class DataBase:
    def __init__(self):
        self.sqlite_connection = sqlite3.connect('logins.db', check_same_thread=False)
        self.cursor = self.sqlite_connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = '''select * from users limit 1 '''
            result = self.cursor.execute(query).fetchone()
        except sqlite3.OperationalError:
            query = '''CREATE TABLE "users" ("user_id" INTEGER NOT NULL UNIQUE,"login" TEXT NOT NULL UNIQUE, "password" TEXT NOT NULL, "session" TEXT, "last_activity"	TEXT, PRIMARY KEY("user_id" AUTOINCREMENT))'''
            self.cursor.execute(query)

    def get_user(self, login):
        query = '''SELECT * from users WHERE login=?'''
        print(login, query)
        result = self.cursor.execute(query, (login,)).fetchone()
        print(result)
        if result is not None:
            return dict(user_id=result[0], login=result[1],
                        password=result[2], session=result[3], last_activity=result[4])
        else:
            return result

    def add_user(self, login, password):
        if self.get_user(login) is None:
            for_hash = login + str(datetime.now())
            ciphertext = md5(for_hash.encode('utf-8')).hexdigest()
            activ = str(datetime.now())
            query = '''INSERT into users(login,password,session,last_activity) VALUES (?, ?,?,?)'''
            self.cursor.execute(query, (login, password, ciphertext, activ))
            self.sqlite_connection.commit()
            return self.get_user(login)

    def update_session(self, login):
        if self.get_user(login) is not None:
            for_hash = login + str(datetime.now())
            ciphertext1 = md5(for_hash.encode('utf-8')).hexdigest()
            query = '''UPDATE  users SET session= ? WHERE login=?'''
            self.cursor.execute(query, (ciphertext1, login))
            self.sqlite_connection.commit()

    def update_activity(self, login):
        if self.get_user(login) is not None:
            query = '''UPDATE users SET last_activity=? WHERE login=?'''
            self.cursor.execute(query, (str(datetime.now()), login))
            self.sqlite_connection.commit()

    def close(self):
        self.sqlite_connection.close()


if __name__ == '__main__':
    d = DataBase()
    ##print(d.get_user('user')['password']=="dasdsadsadasd")
    login = input()
    password = input()
    d.add_user(login, password)
    d.update_session(login)
    d.update_activity(login)
    print(d.get_user(login))
