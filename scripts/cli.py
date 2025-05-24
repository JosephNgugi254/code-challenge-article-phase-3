# scripts/cli.py
import cmd
from lib.models.author import Author
from lib.models.magazine import Magazine
from lib.models.article import Article
from scripts.run_queries import *

class ArticlesCLI(cmd.Cmd):
    prompt = "Articles> "

    def do_create_author(self, arg):
        """Create a new author: create_author <name>"""
        try:
            author = Author(arg)
            print(f"Created author: {author.name} (ID: {author.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def do_create_magazine(self, arg):
        """Create a new magazine: create_magazine <name> <category>"""
        args = arg.split()
        if len(args) != 2:
            print("Usage: create_magazine <name> <category>")
            return
        try:
            magazine = Magazine(args[0], args[1])
            print(f"Created magazine: {magazine.name} (ID: {magazine.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def do_create_article(self, arg):
        """Create a new article: create_article <title> <author_id> <magazine_id>"""
        args = arg.split(maxsplit=2)
        if len(args) != 3:
            print("Usage: create_article <title> <author_id> <magazine_id>")
            return
        try:
            article = Article(args[0], int(args[1]), int(args[2]))
            print(f"Created article: {article.title} (ID: {article.id})")
        except ValueError as e:
            print(f"Error: {e}")

    def do_list_articles(self, arg):
        """List articles for an author: list_articles <author_id>"""
        try:
            author = Author.find_by_id(int(arg))
            if author:
                articles = author.articles()
                for a in articles:
                    print(f"- {a.title} (Magazine ID: {a.magazine_id})")
            else:
                print("Author not found")
        except ValueError:
            print("Invalid author ID")

    def do_top_publisher(self, arg):
        """Show magazine with most articles"""
        top = Magazine.top_publisher()
        print(f"Top publisher: {top.name} ({top.category})" if top else "No magazines")

    def do_exit(self, arg):
        """Exit the CLI"""
        return True

if __name__ == "__main__":
    ArticlesCLI().cmdloop()