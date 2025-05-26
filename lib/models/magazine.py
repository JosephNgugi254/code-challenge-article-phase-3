# lib/models/magazine.py
from lib.db.connection import get_connection
from lib.models.article import Article
from lib.models.author import Author

class Magazine:
    def __init__(self, name, category, id=None):
        if not name:
            raise ValueError("Name cannot be empty")
        self._name = name
        self._category = category
        self._id = id
        if not id:
            self._save()

    def _save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)",
                      (self._name, self._category))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines WHERE id = ?", (id,))
        row = cursor.fetchone()
        print(f"Magazine.find_by_id({id}):", dict(row) if row else None)
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None

    def articles(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row['title'], row['author_id'], row['magazine_id'], row['id']) for row in rows]

    def contributors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT au.* FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in rows]

    def contributing_authors(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT au.* FROM authors au
            JOIN articles a ON a.author_id = au.id
            WHERE a.magazine_id = ?
            GROUP BY au.id
            HAVING COUNT(a.id) > 2
        """, (self._id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row['name'], row['id']) for row in rows]

    @classmethod
    def top_publisher(cls):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        print("Articles in top_publisher:", [(row['id'], row['title']) for row in cursor.fetchall()])
        cursor.execute("SELECT * FROM magazines")
        print("Magazines in top_publisher:", [(row['id'], row['name']) for row in cursor.fetchall()])
        cursor.execute("""
            SELECT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            GROUP BY m.id
            ORDER BY COUNT(a.id) DESC
            LIMIT 1
        """)
        row = cursor.fetchone()
        print("Top publisher row:", dict(row) if row else None)
        conn.close()
        return cls(row['name'], row['category'], row['id']) if row else None