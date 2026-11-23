import sqlite3
import os
from pathlib import Path

# Database file location
DB_PATH = os.path.join(os.path.dirname(__file__), 'complaint_system.db')

def get_db():
    """Get SQLite database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Returns rows as dictionaries
    return conn

def init_db():
    """Initialize database with schema"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Categories table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE,
            description TEXT
        )
    ''')
    
    # Complaints table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT DEFAULT 'open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(user_id),
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    ''')
    
    # Status logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS status_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            complaint_id INTEGER NOT NULL,
            updated_by INTEGER NOT NULL,
            old_status TEXT,
            new_status TEXT,
            remarks TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (complaint_id) REFERENCES complaints(complaint_id),
            FOREIGN KEY (updated_by) REFERENCES users(user_id)
        )
    ''')
    
    conn.commit()
    
    # Insert default categories if they don't exist
    cursor.execute('SELECT COUNT(*) FROM categories')
    if cursor.fetchone()[0] == 0:
        categories = [
            ('Academic', 'Issues related to academics, exams, results'),
            ('Hostel', 'Hostel facility and accommodation issues'),
            ('Transport', 'Bus or transport related complaints'),
            ('Library', 'Library books or facility issues'),
            ('Infrastructure', 'Building and facility maintenance issues'),
            ('Canteen', 'Food quality and canteen service issues'),
            ('Miscellaneous', 'Any other complaint not listed above')
        ]
        cursor.executemany(
            'INSERT INTO categories (category_name, description) VALUES (?, ?)',
            categories
        )
        conn.commit()
    
    cursor.close()
    conn.close()
