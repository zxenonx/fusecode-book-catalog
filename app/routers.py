from fastapi import APIRouter, Depends, Query, status, HTTPException
from sqlalchemy.orm import Session

from . import crud
from .schemas import schemas
from .database import get_db
from .schemas.response import ApiResponse

router = APIRouter()

@router.post("/books/", response_model=ApiResponse[schemas.Book], status_code=201)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
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
            status_code=500
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

@router.get("/books/{book_id}", response_model=ApiResponse[schemas.Book],
            responses={
                404: {
            "description": "Book not found"}
            })
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific book by its ID.

    Args:
        book_id (int): The ID of the book to retrieve.
        db (Session): Db session dependency.

    Returns:
        ApiResponse[schemas.Book]: Response containing the book or error details.
    """
    try:
        book = crud.get_book(db, book_id=book_id)
        if not book:
            response = ApiResponse.not_found_response(resource="Book")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response.model_dump()
            )
            
        return ApiResponse.success_response(
            message="Book retrieved successfully",
            data=book
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse.error_response(
            message="Failed to retrieve book",
            errors=[{"message": str(e)}],
            status_code=500
        )

@router.patch("/books/{book_id}", response_model=ApiResponse[schemas.Book], status_code=200)
def update_book(book_id: int, book: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Updates an existing book in the catalog.

    Args:
        book_id (int): The ID of the book to update.
        book (schemas.BookUpdate): A Pydantic model containing the updated book data.
        db (Session): Db session dependency.

    Returns:
        ApiResponse[schemas.Book]: Response containing the updated book or error details.
    """
    try:
        db_book = crud.update_book(db=db, book_id=book_id, book=book)
        if not db_book:
            response = ApiResponse.not_found_response(resource="Book")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response.model_dump()
            )
        return ApiResponse.success_response(
            message="Book updated successfully",
            data=db_book
        )
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse.error_response(
            message="Failed to update book",
            errors=[{"message": str(e)}],
            status_code=500
        )

@router.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Deletes a book from the catalog.

    Args:
        book_id (int): The ID of the book to delete.
        db (Session): Database session dependency.

    Returns:
        None: 204 No Content on success or error details.
    """
    try:
        db_book = crud.delete_book(db=db, book_id=book_id)
        if not db_book:
            response = ApiResponse.not_found_response(resource="Book")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=response.model_dump()
            )
        return None
    except HTTPException:
        raise
    except Exception as e:
        return ApiResponse.error_response(
            message="Failed to delete book",
            errors=[{"message": str(e)}],
            status_code=500
        )
