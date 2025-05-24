# tests/test_author.py
import pytest
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.db.connection import get_connection

@pytest.fixture
def setup_database():
    conn = get_connection()
    conn.executescript("""
        DELETE FROM articles;
        DELETE FROM authors;
        DELETE FROM magazines;
        INSERT INTO authors (name) VALUES ('Jane Doe');
        INSERT INTO magazines (name, category) VALUES ('Tech Weekly', 'Technology');
        INSERT INTO articles (title, author_id, magazine_id) VALUES ('Test Article', 1, 1);
    """)
    conn.commit()
    conn.close()
    yield
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
    author = Author.find_by_id(1)
    articles = author.articles()
    assert len(articles) == 1
    assert articles[0].title == "Test Article"

def test_author_magazines(setup_database):
    author = Author.find_by_id(1)
    magazines = author.magazines()
    assert len(magazines) == 1
    assert magazines[0].name == "Tech Weekly"

def test_author_topic_areas(setup_database):
    author = Author.find_by_id(1)
    topics = author.topic_areas()
    assert topics == ["Technology"]