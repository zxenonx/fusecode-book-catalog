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
    
    # Check response structure
    assert data["success"] is True
    assert "data" in data
    assert "id" in data["data"]
    
    # Check the returned data matches what we sent
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
    
    # Check error response structure
    assert "errors" in data
    assert len(data["errors"]) > 0  # Should have validation errors


def test_get_books_empty(client):
    """Test getting books when no books exist."""
    response = client.get("/api/v1/books/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    
    # Check response structure
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
    
    # Check response structure
    assert isinstance(data, dict)
    assert "data" in data
    assert isinstance(data["data"], list)
    
    # Check we got the correct number of books
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