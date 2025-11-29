from app import DATABASE
from db import init_db
import sqlite3


def reset_db():
    """
    Delete database tables and start fresh
    """
    con = sqlite3.connect(DATABASE)

    con.execute("DROP TABLE IF EXISTS shapes")
    con.execute("DROP TABLE IF EXISTS places")
    con.close()

    # then call the regular init fn
    init_db()


if __name__ == "__main__":
    reset_db()
    print("db is resetted!")
