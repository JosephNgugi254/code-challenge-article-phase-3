# tests/test_magazine.py
import pytest
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.db.connection import get_connection
from lib.models.magazine import Magazine
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
    jane_id = cursor.lastrowid
    cursor.execute("INSERT INTO authors (name) VALUES (?)", ("John Smith",))
    john_id = cursor.lastrowid
    cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", ("Tech Weekly", "Technology"))
    magazine_id = cursor.lastrowid
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Article 1", jane_id, magazine_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Article 2", john_id, magazine_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Article 3", jane_id, magazine_id))
    cursor.execute("INSERT INTO articles (title, author_id, magazine_id) VALUES (?, ?, ?)", 
                  ("Article 4", jane_id, magazine_id))
    conn.commit()
    
    # Debug
    cursor.execute("SELECT * FROM authors")
    print("Authors:", [(row['id'], row['name']) for row in cursor.fetchall()])
    cursor.execute("SELECT * FROM magazines")
    print("Magazines:", [(row['id'], row['name'], row['category']) for row in cursor.fetchall()])
    cursor.execute("SELECT * FROM articles")
    print("Articles:", [(row['id'], row['title'], row['author_id'], row['magazine_id']) for row in cursor.fetchall()])
    conn.close()
    
    yield {'jane_id': jane_id, 'john_id': john_id, 'magazine_id': magazine_id}
    conn = get_connection()
    conn.executescript("DELETE FROM articles; DELETE FROM authors; DELETE FROM magazines;")
    conn.commit()
    conn.close()

def test_magazine_creation(setup_database):
    magazine = Magazine("Science Monthly", "Science")
    assert magazine.name == "Science Monthly"
    assert magazine.category == "Science"
    assert magazine.id is not None

def test_magazine_invalid_name():
    with pytest.raises(ValueError):
        Magazine("", "Science")

def test_magazine_articles(setup_database):
    ids = setup_database
    magazine = Magazine.find_by_id(ids['magazine_id'])
    articles = magazine.articles()
    assert len(articles) == 4

def test_magazine_contributors(setup_database):
    ids = setup_database
    magazine = Magazine.find_by_id(ids['magazine_id'])
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert {c.name for c in contributors} == {"Jane Doe", "John Smith"}

def test_magazine_contributing_authors(setup_database):
    ids = setup_database
    magazine = Magazine.find_by_id(ids['magazine_id'])
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Jane Doe"

def test_top_publisher(setup_database):
    ids = setup_database
    top = Magazine.top_publisher()
    assert top.name == "Tech Weekly"