# Book Catalog API

A fast CRUD API for managing a book catalog, built with FastAPI, SQLAlchemy, and Python 3.13.

## 🚀 Features

- Create, read, update, and delete books
- RESTful API endpoints
- SQLite database with SQLAlchemy ORM
- Comprehensive test suite
- Built with modern Python tooling (uv, pytest, ruff)

## 🛠️ Prerequisites

- Python 3.13
- [uv](https://docs.astral.sh/uv/getting-started/installation/) - A fast Python package installer and resolver
- [FastAPI](https://fastapi.tiangolo.com/) - For building the API

## 🏗️ Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/zxenonx/fusecode-book-catalog.git
   cd fusecode-book-catalog
   ```

2. **Install Python 3.13**
   ```sh
   uv python install 3.13
   ```

3. **Install dependencies**
   ```sh
   uv sync
   ```
   This will create a virtual environment and install all dependencies listed in `pyproject.toml`.


4. **Activate the virtual environment**
   ```sh
   source .venv/bin/activate  # Linux/macOS
   # .venv\Scripts\activate  # Windows
   ```

## 🚀 Running the Application

Start the development server with hot reload:

```sh
fastapi dev main.py
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

- Interactive API docs: `http://127.0.0.1:8000/docs`
- Alternative API docs: `http://127.0.0.1:8000/redoc`

## 🧪 Running Tests

For detailed testing instructions, see [TESTING.md](tests/TESTING.md).

Run the test suite with:

```sh
uv run pytest -vv
```

For test coverage reports:

```sh
# Terminal coverage report
uv run pytest --cov=app --cov-report=term-missing

# HTML coverage report (generates htmlcov/ directory)
uv run pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser
```

## 🧹 Code Style

This project follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) for docstrings and code formatting.

### Linting

We use [Ruff](https://github.com/charliermarsh/ruff) for fast Python linting and code style enforcement. To check and automatically fix linting issues:

```sh
uv run ruff check . --fix -v
```

This will:
- Check all Python files in the project
- Automatically fix fixable issues

## 🧩 Project Structure

```
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application
│   ├── database.py       # Database configuration
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic models
│   └── routers/          # API routes
├── tests/                # Test files
├── .gitignore
└── pyproject.toml
```

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.