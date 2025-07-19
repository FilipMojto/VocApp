import sqlite3


from schemas import schema_1 as schema

if __name__ == "__main__":
    conn = sqlite3.connect('./vocapp.db')

    cursor = conn.cursor()
    cursor.executescript(schema)
    conn.commit()
    
    cursor.close()
    conn.close()