# scripts/setup_db.py
from lib.db.connection import get_connection

def setup_database():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    conn.close()
    print("Database schema created successfully.")

if __name__ == "__main__":
    setup_database()