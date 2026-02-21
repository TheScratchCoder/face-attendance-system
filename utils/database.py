import sqlite3
from datetime import datetime

DB_PATH = "attendance.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL UNIQUE,
            registered_on TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            roll_no TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT DEFAULT 'Present'
        )
    """)

    conn.commit()
    conn.close()


def mark_attendance(name: str):
    """Mark attendance for a user. Looks up roll_no from users table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Get roll_no
    c.execute("SELECT roll_no FROM users WHERE name = ?", (name,))
    row = c.fetchone()
    roll_no = row[0] if row else "N/A"

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    # Avoid duplicate for same day
    c.execute(
        "SELECT id FROM attendance WHERE name = ? AND date = ?",
        (name, date_str)
    )
    if not c.fetchone():
        c.execute(
            "INSERT INTO attendance (name, roll_no, date, time, status) VALUES (?, ?, ?, ?, ?)",
            (name, roll_no, date_str, time_str, "Present")
        )
        conn.commit()

    conn.close()


def get_attendance(date: str = None):
    """Fetch attendance records. If date is None, return all."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if date:
        c.execute(
            "SELECT * FROM attendance WHERE date = ? ORDER BY time DESC",
            (date,)
        )
    else:
        c.execute("SELECT * FROM attendance ORDER BY date DESC, time DESC")

    rows = c.fetchall()
    conn.close()
    return rows


def get_all_users():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM users ORDER BY registered_on DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def register_user(name: str, roll_no: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute(
            "INSERT INTO users (name, roll_no, registered_on) VALUES (?, ?, ?)",
            (name, roll_no, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()


def delete_user(user_id: int):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
