import sqlite3
from datetime import datetime

def init_db():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS files(
            id INTEGER PRIMARY KEY, 
            file_type TEXT, 
            application_number TEXT, 
            file_date TEXT, 
            oa_start_date TEXT, 
            due_date TEXT, 
            processed_at TEXT
        )
    """)
    con.commit()

def save_file(file_type, application_number, file_date, oa_start_date, due_date):
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    processed_at = datetime.now().isoformat()
    cur.execute("""
        INSERT INTO files (file_type, application_number, file_date, oa_start_date, due_date, processed_at) 
        VALUES(?, ?, ?, ?, ?, ?)
        """, 
        (file_type, application_number, file_date, oa_start_date, due_date, processed_at)
    )
    con.commit()
    con.close()

def get_all_files():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM files")
    res = cur.fetchall()
    con.close()
    return res

if __name__ == "__main__":
    init_db()