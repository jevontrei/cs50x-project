import sqlite3
from db import init_db
from app import DATABASE


def reset_db():
    con = sqlite3.connect(DATABASE)

    con.execute("DROP TABLE IF EXISTS shapes")
    con.execute("DROP TABLE IF EXISTS places")
    con.close()

    # then call init_db()
    init_db()


if __name__ == "__main__":
    reset_db()
    print("db is resetted!")
