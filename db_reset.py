import sqlite3
from db import init_db


def reset_db():
    con = sqlite3.connect("maps.db")
    con.execute("DROP TABLE IF EXISTS shapes")
    con.execute("DROP TABLE IF EXISTS places")
    con.close()

    # then call init_db()
    init_db()


if __name__ == "__main__":
    reset_db()
    print("db is resetted!")
