import sqlite3
import json
from datetime import datetime
from typing import Optional, List, Dict
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

class Database:
    def __init__(self, db_url: str = settings.DATABASE_URL):
        self.db_url = db_url.replace('sqlite:///', '')  # strip prefix
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_url) as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL,
                    status TEXT DEFAULT 'pending',
                    priority INTEGER DEFAULT 5,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    completed_at TIMESTAMP,
                    result TEXT,
                    error TEXT
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS contents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    url TEXT NOT NULL,
                    title TEXT,
                    text TEXT,
                    html TEXT,
                    extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                )
            ''')
            c.execute('''
                CREATE TABLE IF NOT EXISTS media (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    task_id INTEGER,
                    url TEXT NOT NULL,
                    local_path TEXT,
                    file_type TEXT,
                    size INTEGER,
                    downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (task_id) REFERENCES tasks (id)
                )
            ''')
            conn.commit()

    def add_task(self, url: str, priority: int = 5) -> int:
        with sqlite3.connect(self.db_url) as conn:
            c = conn.cursor()
            c.execute('INSERT INTO tasks (url, priority) VALUES (?, ?)', (url, priority))
            return c.lastrowid

    def update_task_status(self, task_id: int, status: str, error: str = None):
        with sqlite3.connect(self.db_url) as conn:
            c = conn.cursor()
            if status == 'completed':
                c.execute('UPDATE tasks SET status=?, completed_at=CURRENT_TIMESTAMP WHERE id=?',
                          (status, task_id))
            else:
                c.execute('UPDATE tasks SET status=?, error=? WHERE id=?', (status, error, task_id))
            conn.commit()

    def save_content(self, task_id: int, url: str, title: str, text: str, html: str):
        with sqlite3.connect(self.db_url) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO contents (task_id, url, title, text, html)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_id, url, title, text, html))
            conn.commit()

    def save_media(self, task_id: int, url: str, local_path: str, file_type: str, size: int):
        with sqlite3.connect(self.db_url) as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO media (task_id, url, local_path, file_type, size)
                VALUES (?, ?, ?, ?, ?)
            ''', (task_id, url, local_path, file_type, size))
            conn.commit()
