import sqlite3


class DataBase:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def get_users(self):
        with self.connection:
            return self.cursor.execute('''SELECT user_id FROM users''').fetchall()

    def users_exist(self, user_id):
        with self.connection:
            result = self.cursor.execute('''SELECT * FROM users WHERE user_id = ?''', (user_id,)).fetchall()
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute('''INSERT INTO users (user_id) VALUES (?)''', (user_id,))

    def get_subscribtions(self, user_id):
        with self.connection:
            return self.cursor.execute('''SELECT subscription_name FROM subscriptions WHERE user_id = ?''', (user_id,)).fetchall()

    def add_subscribtions(self, user_id, subscribe):
        with self.connection:
            return self.cursor.execute('''INSERT INTO subscriptions (user_id, subscription_name) VALUES (?, ?)''', (user_id, subscribe))

    def del_subscribtions(self, user_id, subscribe):
        with self.connection:
            return self.cursor.execute('''DELETE FROM subscriptions WHERE user_id = ? AND subscription_name = ?''', (user_id, subscribe))

    def close(self):
        self.connection.close()