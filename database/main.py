import sqlite3

from schemas import schema

DB_PATH = './vocapp.db'

if __name__ == "__main__":
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()


    cursor.executescript(schema)
    conn.commit()
    conn.close()