# lib/db/connection.py
import sqlite3

def get_connection():
    conn = sqlite3.connect('articles.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn