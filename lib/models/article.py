# lib/models/article.py
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        if not title:
            raise ValueError("Title cannot be empty")
        self._title = title
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._id = id
        if not id:
            self._save()

    def _save(self):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                      (self._title, self._author_id, self._magazine_id))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        print(f"Article.find_by_id({id}):", dict(row) if row else None)
        conn.close()
        return cls(row['title'], row['author_id'], row['magazine_id'], row['id']) if row else None