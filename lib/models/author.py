# lib/models/author.py
from lib.db.connection import get_connection
from lib.models.article import Article

class Author:
    def __init__(self, name, id=None):
        if not name:
            raise ValueError("Name cannot be empty")
        self._name = name
        self._id = id
        if not id:
            self._save()

    def _save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (self._name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors WHERE id = ?", (id,))
        row = cursor.fetchone()
        print(f"Author.find_by_id({id}):", dict(row) if row else None)
        conn.close()
        return cls(row['name'], row['id']) if row else None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE author_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def magazines(self):
        from lib.models.magazine import Magazine  # Lazy import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row['name'], row['category'], row['id']) for row in rows]

    def topic_areas(self):
        from lib.models.magazine import Magazine  # Lazy import
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT m.category FROM magazines m
            JOIN articles a ON a.magazine_id = m.id
            WHERE a.author_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [row['category'] for row in rows]

    def add_article(self, magazine, title):
        """Create an article written by this author for the given magazine."""
        return Article(title, self._id, magazine.id)