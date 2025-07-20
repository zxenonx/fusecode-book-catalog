# Testing - Book Catalog API

## Test Structure

- `tests/test_crud.py`: Unit tests for CRUD operations
- `tests/test_api.py`: Integration tests for API endpoints
- `tests/conftest.py`: Test configuration and fixtures
- `pytest.ini`: Pytest configuration

### Run All Tests

```bash
pytest -vv
```

### Run Specific Test File

```bash
pytest tests/test_api.py -v
```

### Run Specific Test Function

```bash
pytest tests/test_api.py::test_create_book -v
```

### Run with Coverage Report

```bash
# Terminal coverage report
pytest --cov=app --cov-report=term-missing

# HTML coverage report (generates htmlcov/ directory)
pytest --cov=app --cov-report=html
# Open htmlcov/index.html in your browser to view the report
```

### Unit Tests

These test individual components in isolation:
- CRUD operations
- Data validation
- Business logic

### Integration Tests

These test the API endpoints:
- HTTP status codes
- Response formats
- Error handling
- Data validation
