# lib/db/seed.py
import os
import sys
# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from lib.db.connection import get_connection

def seed_database():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        conn.execute("BEGIN TRANSACTION")
        # Insert authors
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Jane Doe",))
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("John Smith",))
        cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Alice Brown",))
        # Insert magazines
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Science Monthly", "Science"))
        # Insert articles
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                      ("AI Revolution", 1, 1))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                      ("Quantum Computing", 1, 2))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                      ("Tech Trends", 2, 1))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                      ("Climate Change", 3, 2))
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                      ("Data Science", 1, 1))
        conn.execute("COMMIT")
        print("Database seeded successfully.")
    except Exception as e:
        conn.execute("ROLLBACK")
        print(f"Failed to seed database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    seed_database()