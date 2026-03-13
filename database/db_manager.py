import sqlite3
from config.config import DATABASE_PATH

class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
        self._create_tables()

    def _create_tables(self):
        # Appointments table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            date TEXT,
            time TEXT,
            reason TEXT,
            status TEXT DEFAULT 'Scheduled'
        )""")
        
        # Long-term Chat Memory table
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS chat_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT,
            role TEXT,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )""")
        
        # Topic tracking
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS topics (
            topic TEXT,
            id INTEGER PRIMARY KEY AUTOINCREMENT
        )""")
        
        self.conn.commit()
        try:
            self.conn.execute("ALTER TABLE appointments ADD COLUMN user_name TEXT")
            self.conn.commit()
        except: pass

    def add_appointment(self, name, date, time, reason):
        self.conn.execute("INSERT INTO appointments (user_name, date, time, reason) VALUES (?, ?, ?, ?)", (name, date, time, reason))
        self.conn.commit()

    def save_chat_message(self, user_name, role, content):
        self.conn.execute("INSERT INTO chat_memory (user_name, role, content) VALUES (?, ?, ?)", (user_name, role, content))
        self.conn.commit()

    def get_chat_history(self, user_name):
        return self.conn.execute("SELECT role, content FROM chat_memory WHERE user_name = ? ORDER BY id ASC", (user_name,)).fetchall()

    def log_topic(self, topic):
        self.conn.execute("INSERT INTO topics (topic) VALUES (?)", (topic,))
        self.conn.commit()

    def get_top_topics(self):
        return self.conn.execute("SELECT topic, COUNT(*) as count FROM topics GROUP BY topic ORDER BY count DESC LIMIT 5").fetchall()

    def get_query_stats(self):
        return self.conn.execute("SELECT COUNT(*) FROM chat_memory WHERE role = 'user'").fetchone()[0]

    def get_appointment_stats(self):
        return self.conn.execute("SELECT COUNT(*) FROM appointments").fetchone()[0]

    def clear_history_for_user(self, user_name):
        self.conn.execute("DELETE FROM chat_memory WHERE user_name = ?", (user_name,))
        self.conn.commit()

    def get_total_users_count(self):
        return self.conn.execute("SELECT COUNT(DISTINCT user_name) FROM chat_memory").fetchone()[0]
    
