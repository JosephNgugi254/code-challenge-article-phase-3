# lib/debug.py
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from scripts.run_queries import *

def debug():
    print("Interactive debugging session")
    # Example usage
    author = Author("Debug Author")
    magazine = Magazine("Debug Mag", "Debugging")
    article = author.add_article(magazine, "Debug Article")
    print(f"Created author: {author.name}, magazine: {magazine.name}, article: {article.title}")
    print("Authors for magazine 1:", [a.name for a in authors_for_magazine(1)])
    print("Top publisher:", Magazine.top_publisher().name if Magazine.top_publisher() else None)

if __name__ == "__main__":
    debug()