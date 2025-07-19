from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.database import engine
import app.models as models
from app.routers import router
from app.schemas.response import ApiResponse

from contextlib import asynccontextmanager

import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Book Catalog API",
    description="A FastAPI book catalog API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors and format them in the standard API response format."""
    errors = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        errors.append({
            "field": field if field else "body",
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=ApiResponse.error_response(
            message="Validation error",
            errors=errors,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        ).model_dump()
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled exceptions.

    Args:
        request (Request): The HTTP request that caused the exception
        exc (Exception): The exception that was raised

    Returns:
        JSONResponse: Standardized error response
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=ApiResponse.error_response(
            message="Internal server error",
            errors=[{"message": "An unexpected error occurred"}],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        ).model_dump()
    )

app.include_router(router, prefix="/api/v1", tags=["Books"])

@app.get("/")
async def root():
    """Root endpoint for API health check."""
    return {
        "message": "Book Catalog API is running",
        "status": "running",
        "version": "1.0.0",
    }