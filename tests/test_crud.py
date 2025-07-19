import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app import crud
from app.schemas.schemas import BookCreate

# Test data
TEST_BOOK_DATA = {
    "title": "Test Book",
    "author": "Test Author",
    "published_year": 2023,
    "summary": "A test book for unit testing"
}

def test_create_book_success(db_session: Session):
    """Test creating a book with all required fields."""
    # Arrange
    book_data = BookCreate(**TEST_BOOK_DATA)
    
    # Act
    created_book = crud.create_book(db_session, book=book_data)
    
    # Assert
    assert created_book is not None
    assert created_book.id is not None
    assert created_book.title == TEST_BOOK_DATA["title"]
    assert created_book.author == TEST_BOOK_DATA["author"]
    assert created_book.published_year == TEST_BOOK_DATA["published_year"]
    assert created_book.summary == TEST_BOOK_DATA["summary"]

def test_create_book_with_optional_fields(db_session: Session):
    """Test creating a book with optional fields."""
    # Arrange
    book_data = BookCreate(
        title="Book with Optional Fields",
        author="Optional Author",
        published_year=2022,
        summary="This is an optional summary"
    )
    
    # Act
    created_book = crud.create_book(db_session, book=book_data)
    
    # Assert
    assert created_book is not None
    assert created_book.summary == "This is an optional summary"

def test_create_book_required_fields_only(db_session: Session):
    """Test creating a book with only required fields."""
    # Arrange
    book_data = BookCreate(
        title="Required Fields Only",
        author="Required Author",
        published_year=2021
    )
    
    # Act
    created_book = crud.create_book(db_session, book=book_data)
    
    # Assert
    assert created_book is not None
    assert created_book.summary is None

def test_create_book_edge_case_year(db_session: Session):
    """Test creating a book with edge case years."""
    min_year = 1000
    book_data = BookCreate(
        title="Old Book",
        author="Ancient Author",
        published_year=min_year
    )
    
    book = crud.create_book(db_session, book=book_data)
    assert book.published_year == min_year
    
    # Test with current year
    current_year = datetime.now().year
    book_data = BookCreate(
        title="Current Year Book",
        author="Current Author",
        published_year=current_year
    )
    
    book = crud.create_book(db_session, book=book_data)
    assert book.published_year == current_year

    # Test with future year raises validation error
    future_year = datetime.now().year + 1
    with pytest.raises(ValueError) as exc_info:
        book_data = BookCreate(
            title="Future Year Book",
            author="Future Author",
            published_year=future_year
        )
        crud.create_book(db_session, book=book_data)

    assert f"Input should be less than or equal to {current_year}" in str(exc_info.value)


def test_get_books_empty(db_session: Session):
    """Test getting books when no books exist."""
    books = crud.get_books(db_session)
    assert len(books) == 0


def test_get_books_with_pagination(db_session: Session):
    """Test getting books with pagination."""
    # Create test data
    test_books = [
        BookCreate(
            title=f"Book {i}",
            author=f"Author {i}",
            published_year=2000 + i,
            summary=f"Summary {i}"
        )
        for i in range(1, 11)  # Create 10 test books
    ]
    
    # Add books to db
    for book_data in test_books:
        crud.create_book(db_session, book=book_data)
    
    # Test pagination
    # First page (first 5 books)
    books = crud.get_books(db_session, skip=0, limit=5)
    assert len(books) == 5
    assert books[0].title == "Book 1"
    assert books[4].title == "Book 5"
    
    # Second page (next 5 books)
    books = crud.get_books(db_session, skip=5, limit=5)
    assert len(books) == 5
    assert books[0].title == "Book 6"
    assert books[4].title == "Book 10"
    
    # Test with limit larger than available
    books = crud.get_books(db_session, skip=0, limit=20)
    assert len(books) == 10
    
    # Test with skip beyond available
    books = crud.get_books(db_session, skip=15, limit=5)
    assert len(books) == 0