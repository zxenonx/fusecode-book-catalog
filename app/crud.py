from sqlalchemy.orm import Session
from . import models
from .schemas import schemas

def get_book(db: Session, book_id: int):
    """Retrieves a book record from the db by its ID.

    Args:
        db (Session): Db session for executing db operations.
        book_id (int): The ID of the book record to retrieve.

    Returns:
        models.Book: The book record with the specified ID, or None if not found.
    """
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 100):
    """Retrieves a list of book records from the db.

    Args:
        db (Session): Db session for executing db operations.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[models.Book]: A list of book records.
    """
    return db.query(models.Book).offset(skip).limit(limit).all()

def create_book(db: Session, book: schemas.BookCreate):
    """Creates a new book record in the database.

    Args:
        db (Session): Db session for executing database operations.
        book (schemas.BookCreate): A Pydantic model containing the book data to be created.

    Returns:
        models.Book: The newly created book record.
    """
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


def update_book(db: Session, book_id: int, book: schemas.BookUpdate):
    """Updates an existing book record in the db.

    Args:
        db (Session): Db session for executing db operations.
        book_id (int): The ID of the book record to update.
        book (schemas.BookUpdate): A Pydantic model containing the updated book data.

    Returns:
        models.Book: The updated book record.
    """
    db_book = get_book(db, book_id)
    if db_book:
        update_data = book.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book


def delete_book(db: Session, book_id: int):
    """Deletes a book record from the db.

    Args:
        db (Session): Db session for executing db operations.
        book_id (int): The ID of the book record to delete.

    Returns:
        models.Book: The deleted book record, or None if not found.
    """
    db_book = get_book(db, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
    return db_book
