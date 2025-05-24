# lib/models/article.py
from lib.db.connection import get_connection

class Article:
    def __init__(self, title, author_id, magazine_id, id=None):
        self._id = id
        self._title = None
        self._author_id = author_id
        self._magazine_id = magazine_id
        self.title = title
        if id is None:
            self.save()

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            if self._id is None:
                cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)",
                              (self._title, self._author_id, self._magazine_id))
                self._id = cursor.lastrowid
                conn.commit()
            else:
                cursor.execute("UPDATE articles SET title = ?, author_id = ?, magazine_id = ? WHERE id = ?",
                              (self._title, self._author_id, self._magazine_id, self._id))
                conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    @classmethod
    def find_by_id(cls, id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE id = ?", (id,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['title'], row['author_id'], row['magazine_id'], row['id']) if row else None

    @classmethod
    def find_by_title(cls, title):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE title = ?", (title,))
        row = cursor.fetchone()
        conn.close()
        return cls(row['title'], row['author_id'], row['magazine_id'], row['id']) if row else None