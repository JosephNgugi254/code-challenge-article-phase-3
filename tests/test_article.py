# tests/test_article.py
import pytest
from lib.models.article import Article
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

def test_article_creation(setup_database):
    article = Article("New Article", 1, 1)
    assert article.title == "New Article"
    assert article.author_id == 1
    assert article.magazine_id == 1
    assert article.id is not None

def test_article_invalid_title():
    with pytest.raises(ValueError):
        Article("", 1, 1)

def test_article_find_by_id(setup_database):
    article = Article.find_by_id(1)
    assert article.title == "Test Article"