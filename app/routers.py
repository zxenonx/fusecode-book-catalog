from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from . import crud
from .schemas import schemas
from .database import get_db
from .schemas.response import ApiResponse

router = APIRouter()

@router.post("/books/", response_model=ApiResponse[schemas.Book], status_code=201)
async def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Creates a new book in the catalog.

    Args:
        book (schemas.BookCreate): A Pydantic model containing the book data to be created.
        db (Session, optional): Database session dependency.

    Returns:
        ApiResponse[schemas.Book]: Response containing the created book or error details.
    """
    try:
        db_book = crud.create_book(db=db, book=book)
        return ApiResponse.created_response(
            message="Book created successfully",
            data=db_book
        )
    except Exception as e:
        return ApiResponse.error_response(
            message="Failed to create book",
            errors=[{"message": str(e)}],
            status_code=400
        )

@router.get("/books/", response_model=ApiResponse[list[schemas.Book]])
async def get_books(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    db: Session = Depends(get_db)
):
    """Retrieves a paginated list of all books in the catalog.

    Args:
        skip (int): Number of records to skip (for pagination).
        limit (int): Maximum number of records to return (for pagination).
        db (Session): Db session dependency.

    Returns:
        ApiResponse[list[schemas.Book]]: Response containing the list of books.
    """
    try:
        books = crud.get_books(db, skip=skip, limit=limit)
        return ApiResponse.success_response(
            message="Books retrieved successfully",
            data=books
        )
    except Exception as e:
        return ApiResponse.error_response(
            message="Failed to retrieve books",
            errors=[{"message": str(e)}],
            status_code=500
        )
