# tests/test_article.py
import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.db.connection import get_connection
from lib.models.article import Article

@pytest.fixture
def setup_database():
    conn = get_connection()
    with open('lib/db/schema.sql', 'r') as f:
        schema = f.read()
    conn.executescript(schema)
    conn.commit()
    
    cursor = conn.cursor()
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("Jane Doe",))
    author_id = cursor.lastrowid
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
    magazine_id = cursor.lastrowid
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Test Article", author_id, magazine_id))
    article_id = cursor.lastrowid
    conn.commit()
    
    # Debug
    cursor.execute("SELECT * FROM authors")
    print("Authors:", [(row['id'], row['name']) for row in cursor.fetchall()])
    cursor.execute("SELECT * FROM magazines")
    print("Magazines:", [(row['id'], row['name'], row['category']) for row in cursor.fetchall()])
    cursor.execute("SELECT * FROM articles")
    print("Articles:", [(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in cursor.fetchall()])
    conn.close()
    
    yield {'author_id': author_id, 'magazine_id': magazine_id, 'article_id': article_id}
    conn = get_connection()
    conn.executescript("DELETE FROM articles; DELETE FROM authors; DELETE FROM magazines;")
    conn.commit()
    conn.close()

def test_article_creation(setup_database):
    ids = setup_database
    article = Article("New Article", ids['author_id'], ids['magazine_id'])
    assert article.title == "New Article"
    assert article.author_id == ids['author_id']
    assert article.magazine_id == ids['magazine_id']
    assert article.id is not None

def test_article_invalid_title():
    with pytest.raises(ValueError):
        Article("", 1, 1)

def test_article_find_by_id(setup_database):
    ids = setup_database
    article = Article.find_by_id(ids['article_id'])
    assert article.title == "Test Article"