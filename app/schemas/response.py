from typing import TypeVar, Generic, Optional, Any, Union
from pydantic import BaseModel, ConfigDict, Field
from fastapi import status

class ErrorDetail(BaseModel):
    """Schema for error details in the API response."""
    field: Optional[str] = Field(
        None,
        description="The field that caused the error"
    )
    message: str = Field(
        ...,
        description="A human-readable error message"
    )
    type: Optional[str] = Field(
        None,
        description="The type or category of error"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "field": "title",
                "message": "String should have at least 1 character",
                "type": "string_too_short"
            }
        }
    )

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    """Standard API response format.
    
    This is a generic response wrapper that can contain any type of data.
    """
    success: bool = Field(..., description="Indicates if the request was successful")
    message: str = Field(
        ...,
        description="Human-readable message about the response",)
    data: Optional[T] = Field(
        None,
        description="The response payload"
    )
    errors: Optional[list[ErrorDetail]] = Field(
        None,
        description="List of error details if any"
    )
    status_code: Optional[int] = Field(
        None,
        description="HTTP status code of the response"
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {
                    "id": 1,
                    "title": "The thing around your neck",
                    "author": "Chimamanda Ngozi Adichie",
                    "published_year": 2009,
                    "summary": "A sample book description"
                },
                "errors": None,
                "status_code": 200
            }
        }
    )

    @classmethod
    def success_response(
        cls,
        message: str = "Operation completed successfully",
        data: Optional[Any] = None,
        status_code: int = status.HTTP_200_OK
    ) -> 'ApiResponse':
        """Create a success response.
        
        Args:
            message: Success message
            data: Response data
            status_code: HTTP status code (default: 200 OK)
            
        Returns:
            Formatted success response
        """
        return cls(
            success=True,
            message=message,
            data=data,
            errors=None,
            status_code=status_code
        )
        
    @classmethod
    def created_response(
        cls,
        message: str = "Resource created successfully",
        data: Optional[Any] = None
    ) -> 'ApiResponse':
        """Create a 201 Created response.
        
        Args:
            message: Success message
            data: The created resource
            
        Returns:
            Formatted 201 response
        """
        return cls.success_response(
            message=message,
            data=data,
            status_code=status.HTTP_201_CREATED
        )

    @classmethod
    def error_response(
        cls,
        message: str = "An error occurred",
        errors: Optional[list[Union[dict[str, Any], ErrorDetail]]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST
    ) -> 'ApiResponse':
        """Create an error response.
        
        Args:
            message: Error message
            errors: List of error details as dictionaries or ErrorDetail objects
            status_code: HTTP status code (default: 400 Bad Request)
            
        Returns:
            Formatted error response
        """
        if errors is None:
            errors = [ErrorDetail(message=message)]
        else:
            errors = [
                error if isinstance(error, ErrorDetail) else ErrorDetail(**error)
                for error in errors
            ]
            
        return cls(
            success=False,
            message=message,
            data=None,
            errors=errors,
            status_code=status_code
        )

    @classmethod
    def not_found_response(
        cls,
        resource: str = "Resource"
    ) -> 'ApiResponse':
        """Create a 404 not found response.
        
        Args:
            resource: Name of the resource that wasn't found
            
        Returns:
            Formatted 404 response
        """
        return cls.error_response(
            message=f"{resource} not found",
            status_code=status.HTTP_404_NOT_FOUND
        )
