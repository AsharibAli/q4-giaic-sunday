"""Pydantic models for file upload API."""

from datetime import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel, Field


class FileType(str, Enum):
    """File category enum."""

    IMAGE = "image"
    VIDEO = "video"


class UploadedFile(BaseModel):
    """Response model for a successfully uploaded file."""

    storage_key: str = Field(..., description="Unique identifier in R2 storage")
    original_filename: str = Field(..., max_length=255, description="Original filename provided by user")
    file_type: FileType = Field(..., description="Category of file")
    mime_type: str = Field(..., description="MIME type of the file")
    size_bytes: int = Field(..., ge=1, description="File size in bytes")
    uploaded_at: datetime = Field(..., description="UTC timestamp of upload")
    url: str = Field(..., description="Shareable URL for the file")


class ErrorCode(str, Enum):
    """Error codes for API responses."""

    INVALID_FILE_TYPE = "INVALID_FILE_TYPE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    STORAGE_ERROR = "STORAGE_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"


class Error(BaseModel):
    """Error details."""

    code: ErrorCode = Field(..., description="Error code for programmatic handling")
    message: str = Field(..., description="Human-readable error message")


class ErrorResponse(BaseModel):
    """Error response wrapper."""

    error: Error


class FailedUpload(BaseModel):
    """Details of a failed upload in batch operations."""

    filename: str = Field(..., description="Original filename of failed file")
    error: Error


class BatchUploadResponse(BaseModel):
    """Response model for batch upload operations."""

    successful: list[UploadedFile] = Field(default_factory=list, description="Successfully uploaded files")
    failed: list[FailedUpload] = Field(default_factory=list, description="Files that failed to upload")
    total: int = Field(..., description="Total number of files in request")


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""

    status: Literal["healthy", "unhealthy"] = Field(..., description="Overall service health")
    timestamp: datetime = Field(..., description="Health check timestamp")
    services: dict[str, Literal["connected", "disconnected"]] | None = Field(
        default=None, description="Status of dependent services"
    )
