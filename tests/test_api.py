from fastapi import status

# Test data
TEST_BOOK_DATA = {
    "title": "Test Book",
    "author": "Test Author",
    "published_year": 2023,
    "summary": "A test book for integration testing"
}

def test_create_book(client):
    """Test creating a valid book."""
    response = client.post("/api/v1/books/", json=TEST_BOOK_DATA)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    
    # Verify the response
    assert data["success"] is True
    assert "data" in data
    assert "id" in data["data"]

    assert data["data"]["title"] == TEST_BOOK_DATA["title"]
    assert data["data"]["author"] == TEST_BOOK_DATA["author"]
    assert data["data"]["published_year"] == TEST_BOOK_DATA["published_year"]
    assert data["data"]["summary"] == TEST_BOOK_DATA["summary"]


def test_create_book_invalid_data(client):
    """Test creating a book with invalid data."""
    # Missing required fields
    response = client.post("/api/v1/books/", json={"title": ""})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()
    
    # Check error response
    assert "errors" in data
    assert len(data["errors"]) > 0


def test_get_books_empty(client):
    """Test getting books when no books exist."""
    response = client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)

    assert len(data["data"]) == 0

def test_get_books_with_data(client):
    """Test getting books when books exist in the db."""
    response = client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 0

    test_books = [
        {
            "title": f"Book {i}",
            "author": f"Author {i}",
            "published_year": 2000 + i,
            "summary": f"Summary {i}"
        }
        for i in range(1, 11)
    ]
    
    # Add books through the API
    for book_data in test_books:
        response = client.post("/api/v1/books/", json=book_data)
        assert response.status_code == status.HTTP_201_CREATED
    
    # Test pagination - 1st page
    response = client.get("/api/v1/books/", params={"skip": 0, "limit": 5})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)

    assert len(data["data"]) == 5
    
    # Check the first book's data
    first_book = data["data"][0]
    assert first_book["title"] == "Book 1"
    assert first_book["author"] == "Author 1"
    assert first_book["published_year"] == 2001
    assert first_book["summary"] == "Summary 1"
    
    # Test pagination - 2nd page
    response = client.get("/api/v1/books/", params={"skip": 5, "limit": 5})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data["data"]) == 5
    assert data["data"][0]["title"] == "Book 6"
    assert data["data"][4]["title"] == "Book 10"


def test_get_book_success(client):
    """Test retrieving an existing book by ID."""
    create_response = client.post("/api/v1/books/", json={**TEST_BOOK_DATA})

    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["data"]["id"]

    # Retrieve the book
    response = client.get(f"/api/v1/books/{book_id}")
    assert response.status_code == status.HTTP_200_OK

    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Book retrieved successfully"
    assert data["data"]["id"] == book_id
    assert data["data"]["title"] == "Test Book"
    assert data["data"]["author"] == "Test Author"
    assert data["data"]["published_year"] == 2023
    assert data["data"]["summary"] == "A test book for integration testing"


def test_get_book_not_found(client):
    """Test retrieving a non-existent book by ID."""
    response = client.get("/api/v1/books/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

    data = response.json()["detail"]
    assert data["success"] is False
    assert data["message"] == "Book not found"
    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["message"] == "Book not found"

def test_update_book_success(client):
    """Test successfully updating an existing book."""
    # Create a book
    create_response = client.post("/api/v1/books/", json=TEST_BOOK_DATA)
    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["data"]["id"]
    
    # Update the book
    update_data = {
        "title": "Updated Test Book",
        "author": "Updated Test Author",
        "published_year": 2024,
        "summary": "Updated test book summary"
    }
    response = client.patch(f"/api/v1/books/{book_id}", json=update_data)
    
    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["success"] is True
    assert data["message"] == "Book updated successfully"
    assert data["data"]["id"] == book_id
    assert data["data"]["title"] == update_data["title"]
    assert data["data"]["author"] == update_data["author"]
    assert data["data"]["published_year"] == update_data["published_year"]
    assert data["data"]["summary"] == update_data["summary"]
    
    # Verify the book was actually updated in the db
    get_response = client.get(f"/api/v1/books/{book_id}")
    assert get_response.status_code == status.HTTP_200_OK
    book_data = get_response.json()["data"]

    assert book_data["title"] == update_data["title"]
    assert book_data["author"] == update_data["author"]
    assert book_data["published_year"] == update_data["published_year"]
    assert book_data["summary"] == update_data["summary"]


def test_update_book_partial(client):
    """Test updating only specific fields of a book."""
    # Create a book
    create_response = client.post("/api/v1/books/", json=TEST_BOOK_DATA)
    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["data"]["id"]
    
    # Update only the title and summary
    update_data = {
        "title": "Partially Updated Title",
        "summary": "Updated summary only"
    }
    response = client.patch(f"/api/v1/books/{book_id}", json=update_data)
    
    # Verify the response
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data["success"] is True
    assert data["data"]["id"] == book_id
    assert data["data"]["title"] == update_data["title"]
    assert data["data"]["author"] == TEST_BOOK_DATA["author"]
    assert data["data"]["published_year"] == TEST_BOOK_DATA["published_year"]
    assert data["data"]["summary"] == update_data["summary"]


def test_update_book_not_found(client):
    """Test updating a non-existent book returns 404."""
    update_data = {
        "title": "Non-existent Book",
        "author": "Unknown Author"
    }
    response = client.patch("/api/v1/books/999999", json=update_data)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()["detail"]
    assert data["success"] is False
    assert data["message"] == "Book not found"
    assert "errors" in data
    assert len(data["errors"]) > 0


def test_update_book_invalid_data(client):
    """Test updating a book with invalid data returns 422."""
    # Create a book
    create_response = client.post("/api/v1/books/", json=TEST_BOOK_DATA)
    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["data"]["id"]
    
    # Update with invalid data
    invalid_data = {
        "published_year": -2023,
        "title": ""
    }
    response = client.patch(f"/api/v1/books/{book_id}", json=invalid_data)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    data = response.json()

    assert "errors" in data
    assert len(data["errors"]) >= 0


def test_delete_book_success(client):
    """Test successfully deleting an existing book."""
    # Create a book to
    create_response = client.post("/api/v1/books/", json=TEST_BOOK_DATA)
    assert create_response.status_code == status.HTTP_201_CREATED
    book_id = create_response.json()["data"]["id"]
    
    # Delete the book
    response = client.delete(f"/api/v1/books/{book_id}")
    
    # Verify the response
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not response.content
    
    # Verify the book was actually deleted from the db
    get_response = client.get(f"/api/v1/books/{book_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_book_not_found(client):
    """Test deleting a non-existent book returns 404."""
    response = client.delete("/api/v1/books/999999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    data = response.json()["detail"]

    assert data["success"] is False
    assert data["message"] == "Book not found"
    assert "errors" in data
    assert len(data["errors"]) > 0
    assert data["errors"][0]["message"] == "Book not found"
