# init_db.py
# [Inisialisasi DB admin dan user + admin dan user awal]
import sqlite3
import bcrypt

conn = sqlite3.connect("facepay.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS log (
    id INTEGER PRIMARY KEY,
    user TEXT,
    action TEXT,
    amount INTEGER,
    timestamp TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS login_log (
    id INTEGER PRIMARY KEY,
    user TEXT,
    timestamp TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT
)
""")

pwd = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
c.execute("INSERT OR IGNORE INTO admin (id, username, password) VALUES (1, 'admin', ?)", (pwd,))

conn.commit()
conn.close()
