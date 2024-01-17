import sqlite3
from argon2 import PasswordHasher

class DatabaseHandler:

    GET_USER = "SELECT * FROM users WHERE username = ?"
    GET_PASSWORD = "SELECT password FROM users WHERE username = ?"
    CREATE_USER = "INSERT INTO users(username, password) VALUES (?, ?)"

    def __init__(self):
        self.conn = sqlite3.connect('ext/server.db', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.ph = PasswordHasher()

        # for now
        #self.cur.execute("DELETE FROM users")
        self.conn.commit()

    def user_exists(self, username):
        self.cur.execute(self.GET_USER, (username, ))
        self.conn.commit()

        result = self.cur.fetchone()
        return result is not None

    def validate_password(self, username, password):
        self.cur.execute(self.GET_PASSWORD, (username, ))
        self.conn.commit()

        password_hash = self.cur.fetchone()[0]
        try:
            print(password_hash, password)
            self.ph.verify(password_hash, password)
            return True
        except Exception as c:
            print(c)
            return False

    def create_user(self, username, password, hash_algo):
        password_hash = self.ph.hash(password)
        self.cur.execute(self.CREATE_USER, (username, password_hash))
        self.conn.commit()

    def validate_login(self, username, password):
        self.cur.execute(self.GET_USER, (username, ))
        self.conn.commit()

        user = self.cur.fetchone()
        password_hash = user[2]

        return self.ph.verify(password_hash, password)

database = DatabaseHandler()
