# lib/debug.py
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from lib.models.author import Author
from lib.models.magazine import Magazine

def debug():
    print("Interactive debugging session")
    author = Author("Debug Author")
    magazine = Magazine("Debug Mag", "Debug Category")
    article = author.add_article(magazine, "Debug Article")
    print(f"Created author: {author.name}, magazine: {magazine.name}, article: {article.title}")
    
    # Example query
    authors = magazine.contributors()
    print(f"Authors for magazine {magazine.id}: {[a.name for a in authors]}")
    
    top_mag = Magazine.top_publisher()
    print(f"Top publisher: {top_mag.name if top_mag else 'None'}")

if __name__ == "__main__":
    debug()