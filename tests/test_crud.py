import pytest
from datetime import datetime
from sqlalchemy.orm import Session

from app import crud, models
from app.schemas.schemas import BookCreate, BookUpdate

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

    # Test with future year
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
        for i in range(1, 11)
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

def test_get_book_success(db_session: Session):
    """Test retrieving an existing book by ID."""
    # Create a test book
    test_book = BookCreate(**TEST_BOOK_DATA)
    created_book = crud.create_book(db_session, book=test_book)

    # Retrieve the book by ID
    result = crud.get_book(db_session, book_id=created_book.id)

    assert result is not None
    assert result.id == created_book.id

def test_get_book_not_found(db_session: Session):
    """Test retrieving a non-existent book by ID."""
    # Test with a non-existent ID
    result = crud.get_book(db_session, book_id=9999)
    assert result is None


def test_update_book_success(db_session: Session):
    """Test updating an existing book with valid data."""
    # Create a book
    test_book = BookCreate(**TEST_BOOK_DATA)
    created_book = crud.create_book(db_session, book=test_book)

    update_data = {
        "title": "Updated Title",
        "author": "Updated Author",
        "published_year": 2023,
        "summary": "Updated summary"
    }

    # Perform update
    updated_book = crud.update_book(
        db=db_session,
        book_id=created_book.id,
        book=BookUpdate(**update_data)
    )

    # Verify the update
    assert updated_book is not None
    assert updated_book.id == created_book.id
    assert updated_book.title == "Updated Title"
    assert updated_book.author == "Updated Author"
    assert updated_book.published_year == 2023
    assert updated_book.summary == "Updated summary"


def test_update_book_not_found(db_session: Session):
    """Test updating a non-existent book."""
    update_data = {
        "title": "New Title"
    }

    #Update non-existent book
    result = crud.update_book(
        db=db_session,
        book_id=999,
        book=BookUpdate(**update_data)
    )

    assert result is None


def test_update_book_partial_data(db_session: Session):
    """Test updating only some fields of a book."""
    # Create a book
    test_book = BookCreate(**TEST_BOOK_DATA)
    created_book = crud.create_book(db_session, book=test_book)

    # Update only the title
    updated_book = crud.update_book(
        db=db_session,
        book_id=created_book.id,
        book=BookUpdate(title="New Title Only")
    )

    # Verify only the title was updated
    assert updated_book is not None
    assert updated_book.title == "New Title Only"
    assert updated_book.author == "Test Author"
    assert updated_book.published_year == 2023


def test_delete_book_success(db_session: Session):
    """Test successfully deleting an existing book."""
    # Create a book
    test_book = BookCreate(**TEST_BOOK_DATA)
    created_book = crud.create_book(db_session, book=test_book)
    
    # Delete the book
    deleted_book = crud.delete_book(db=db_session, book_id=created_book.id)

    assert deleted_book is not None
    assert deleted_book.id == created_book.id
    assert deleted_book.title == created_book.title
    assert deleted_book.author == created_book.author
    
    # Verify the book is no longer in the db
    book_in_db = db_session.query(models.Book).filter(models.Book.id == created_book.id).first()
    assert book_in_db is None


def test_delete_book_not_found(db_session: Session):
    """Test deleting a non-existent book returns None."""
    # Delete a non-existent book
    result = crud.delete_book(db=db_session, book_id=999999)

    assert result is None

