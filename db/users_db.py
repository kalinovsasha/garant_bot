import sqlite3
# './db/my_database.db'


class Users_base:
    db_path = './my_database.db'
    access_level: dict = {
        1: "user",
        2: "engineer",
        3: "admin"
    }

    def __init__(self, db_path: str):
        if db_path:
            self.db_path = db_path
        else:
            self.db_path = './my_database.db'
        self.create_base()

    def create_tguser(self, tg_id: int | str, name: str, access_level: int, description: str):
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                "INSERT INTO users (tg_id, name, access_level, description) VALUES (?,?,?,?)", (tg_id, name, access_level, description))

    def read_users(self):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users")
            return cursor.fetchall()

    def read_user(self, tg_id):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users where tg_id=?", (tg_id,))
            return cursor.fetchone()

    def update_tguser(self, tg_id: int | str, name: str, access_level: int, description: str | None):
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, access_level = ?, description = ? WHERE tg_id = ?", (name, access_level, description, tg_id))

    def delete_tguser(self, tg_id: int | str):
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM users WHERE tg_id=?", (tg_id,))

    def delete_iduser(self, id: int | str):
        with sqlite3.connect(self.db_path) as con:
            cursor = con.cursor()
            cursor.execute("DELETE FROM users WHERE id=?", (id,))

    def create_base(self):
        with sqlite3.connect(self.db_path) as connection:
            cursor = connection.cursor()
            cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tg_id INTEGER UNIQUE,
    name TEXT NOT NULL,
    access_level INTEGER,
    description TEXT
)
""")


