import sqlite3
from sqlite3 import Error


class SQLDB:

    def __init__(self, path):
        self.connection = None

        try:
            self.connection = sqlite3.connect(path)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON;")
            self.connection.commit()
        except Error as e:
            print(f"The error {e}")

    def __del__(self):
        self.connection.close()

    def execute_query(self, query: str) -> None:
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Error as e:
            print(f"The error {e} occurred")

    def executemany_query(self, query: str, value: list[tuple]) -> None:
        try:
            self.cursor.executemany(query, value)
            self.connection.commit()
        except Error as e:
            print(f"The error {e} occurred")

    def execute_read_query(self, query: str) -> list:
        result = None
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            return result
        except Error as e:
            print(f"The error {e} occurred")


def create_database():

    sql_db = SQLDB("database.sqlite")

    sql_db.execute_query("DROP TABLE IF EXISTS orders_comic;")
    sql_db.execute_query("DROP TABLE IF EXISTS orders;")
    sql_db.execute_query("DROP TABLE IF EXISTS users;")
    sql_db.execute_query("DROP TABLE IF EXISTS genres_comic;")
    sql_db.execute_query("DROP TABLE IF EXISTS genres;")
    sql_db.execute_query("DROP TABLE IF EXISTS comic;")
    sql_db.execute_query("DROP TABLE IF EXISTS publishers;")
    sql_db.execute_query("DROP TABLE IF EXISTS authors;")

    users_table = """
    CREATE TABLE users (
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        nickname TEXT NOT NULL,
        admin INTEGER NOT NULL DEFAULT 0,
        photo BLOB
    );
    """

    authors_table = """
    CREATE TABLE authors (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fio TEXT NOT NULL,
        bio TEXT,
        photo BLOB
    );
    """

    publishers_table = """
    CREATE TABLE publishers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        contact TEXT,
        logo BLOB
    );
    """

    genres_table = """
    CREATE TABLE genres (
        genre TEXT NOT NULL PRIMARY KEY
    );
    """

    comic_table = """
    CREATE TABLE comic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        authorId INTEGER NOT NULL,
        publisherId INTEGER NOT NULL,
        year TEXT,
        description TEXT,
        image TEXT,
        FOREIGN KEY (authorId) REFERENCES authors (id) ON DELETE CASCADE,
        FOREIGN KEY (publisherId) REFERENCES publishers (id) ON DELETE CASCADE
    );
    """

    genres_comic_table = """
    CREATE TABLE genres_comic (
        comicId INTEGER NOT NULL,
        genre TEXT NOT NULL,
        FOREIGN KEY (comicId) REFERENCES comic (id) ON DELETE CASCADE,
        FOREIGN KEY (genre) REFERENCES genres (genre) ON DELETE CASCADE
    );
    """

    orders_table = """
    CREATE TABLE orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        time TEXT,
        userLogin INTEGER NOT NULL,
        FOREIGN KEY (userLogin) REFERENCES users (login) ON DELETE CASCADE
    );
    """

    orders_comic_table = """
    CREATE TABLE orders_comic (
        comicId INTEGER NOT NULL,
        count INTEGER NOT NULL,
        orderId INTEGER NOT NULL,
        FOREIGN KEY (comicId) REFERENCES comic (id) ON DELETE CASCADE,
        FOREIGN KEY (orderId) REFERENCES orders (id) ON DELETE CASCADE
    );
    """

    sql_db.execute_query(users_table)
    sql_db.execute_query(authors_table)
    sql_db.execute_query(publishers_table)
    sql_db.execute_query(comic_table)
    sql_db.execute_query(genres_table)
    sql_db.execute_query(genres_comic_table)
    sql_db.execute_query(orders_table)
    sql_db.execute_query(orders_comic_table)

    sql_db.execute_query("""INSERT INTO users (nickname, login, password, admin)
        VALUES ('admin', 'admin', '$2b$12$I7ry4Tgnx3Z8.om.S40esOOMgBMNQC2cx5LjuIMH0AGodrLmiVOi6', 1)
    """)


if __name__ == "__main__":
    create_database()
