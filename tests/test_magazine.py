# tests/test_magazine.py
import pytest
from lib.models.magazine import Magazine
from lib.models.author import Author
from lib.db.connection import get_connection

@pytest.fixture
def setup_database():
    conn = get_connection()
    conn.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
        INSERT INTO authors (name) VALUES ('Jane Doe');
        INSERT INTO authors (name) VALUES ('John Smith');
        INSERT INTO magazines (name, category) VALUES ('Tech Weekly', 'Technology');
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Article 1', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Article 2', 2, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Article 3', 1, 1);
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Article 4', 1, 1);
    """)
    conn.commit()
    conn.close()
    yield
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
    magazine = Magazine.find_by_id(1)
    articles = magazine.articles()
    assert len(articles) == 4

def test_magazine_contributors(setup_database):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributors()
    assert len(contributors) == 2
    assert {c.name for c in contributors} == {"Jane Doe", "John Smith"}

def test_magazine_contributing_authors(setup_database):
    magazine = Magazine.find_by_id(1)
    contributors = magazine.contributing_authors()
    assert len(contributors) == 1
    assert contributors[0].name == "Jane Doe"

def test_top_publisher(setup_database):
    top = Magazine.top_publisher()
    assert top.name == "Tech Weekly"