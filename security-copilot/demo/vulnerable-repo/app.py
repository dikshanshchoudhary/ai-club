import sqlite3


DATABASE_PASSWORD = "DEMO_ONLY_NOT_A_REAL_SECRET"


def search_users(query: str):
    connection = sqlite3.connect("demo.db")
    return connection.execute("SELECT * FROM users WHERE name = '" + query + "'").fetchall()

