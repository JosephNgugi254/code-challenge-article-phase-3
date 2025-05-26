# tests/test_author.py
import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.db.connection import get_connection
from lib.models.author import Author

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

def test_author_creation(setup_database):
    author = Author("John Smith")
    assert author.name == "John Smith"
    assert author.id is not None

def test_author_invalid_name():
    with pytest.raises(ValueError):
        Author("")

def test_author_articles(setup_database):
    ids = setup_database
    author = Author.find_by_id(ids['author_id'])
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_database):
    ids = setup_database
    author = Author.find_by_id(ids['author_id'])
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Tech Weekly"

def test_author_topic_areas(setup_database):
    ids = setup_database
    author = Author.find_by_id(ids['author_id'])
    topics = author.topic_areas()
    assert topics == ["Technology"]