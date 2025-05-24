# Object Relations Code Challenge - Articles

A Python project to model Authors, Articles, and Magazines with data stored in a SQL database. Authors can write many articles, magazines can publish many articles, and each article belongs to both an author and a magazine.

## Features

- Python classes for Author, Article, and Magazine with SQL methods
- Many-to-many relationships between authors and magazines via articles
- Raw SQL queries for data access and relationships
- Transaction handling and test coverage

## Setup

1. Clone the repo and install dependencies:
    - With Pipenv:  
      `pipenv install pytest sqlite3 && pipenv shell`
    - Or with venv:  
      `python -m venv env && source env/bin/activate && pip install pytest`
2. Set up the database (SQLite recommended). See `lib/db/connection.py` for details.

## Project Structure

```
code-challenge/
├── lib/
│   ├── models/         # Author, Article, Magazine classes
│   ├── db/             # DB connection, schema, seed data
│   └── controllers/    # (Optional) Business logic
├── tests/              # Pytest test cases
├── scripts/            # Setup and query scripts
└── README.md
```

## Running Tests

- Run `pytest` from the project root to verify your implementation.

## Deliverables

- SQL schema for authors, articles, and magazines
- Python classes with SQL methods and relationship queries
- Transaction handling and error management
- Test coverage for all models


