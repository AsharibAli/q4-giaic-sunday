"""File type and size validation using python-magic."""

from dataclasses import dataclass

import magic

from ..models.upload import ErrorCode, FileType


# Allowed MIME types
ALLOWED_IMAGE_TYPES = frozenset({
    "image/jpeg",
    "image/png",
    "image/gif",
    "image/webp",
})

ALLOWED_VIDEO_TYPES = frozenset({
    "video/mp4",
    "video/webm",
    "video/quicktime",  # MOV
})

ALLOWED_TYPES = ALLOWED_IMAGE_TYPES | ALLOWED_VIDEO_TYPES

# Default size limits (can be overridden via config)
DEFAULT_MAX_IMAGE_SIZE = 100 * 1024 * 1024  # 100MB
DEFAULT_MAX_VIDEO_SIZE = 500 * 1024 * 1024  # 500MB


class FileValidationError(Exception):
    """Exception raised when file validation fails."""

    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message
        super().__init__(message)


@dataclass
class ValidationResult:
    """Result of file validation."""

    mime_type: str
    file_type: FileType
    size_bytes: int


def detect_mime_type(content: bytes) -> str:
    """
    Detect MIME type from file content using libmagic.

    Args:
        content: File content bytes (at least first 2048 bytes)

    Returns:
        Detected MIME type string
    """
    return magic.from_buffer(content[:2048], mime=True)


def get_file_type(mime_type: str) -> FileType | None:
    """
    Determine file type category from MIME type.

    Args:
        mime_type: MIME type string

    Returns:
        FileType enum or None if not allowed
    """
    if mime_type in ALLOWED_IMAGE_TYPES:
        return FileType.IMAGE
    if mime_type in ALLOWED_VIDEO_TYPES:
        return FileType.VIDEO
    return None


def validate_file(
    content: bytes,
    filename: str,
    max_image_size: int = DEFAULT_MAX_IMAGE_SIZE,
    max_video_size: int = DEFAULT_MAX_VIDEO_SIZE,
) -> ValidationResult:
    """
    Validate a file's type and size.

    Args:
        content: Full file content bytes
        filename: Original filename (for error messages)
        max_image_size: Maximum allowed image size in bytes
        max_video_size: Maximum allowed video size in bytes

    Returns:
        ValidationResult with mime_type, file_type, and size_bytes

    Raises:
        FileValidationError: If validation fails
    """
    size_bytes = len(content)

    # Detect MIME type from content
    mime_type = detect_mime_type(content)
    file_type = get_file_type(mime_type)

    # Check if type is allowed
    if file_type is None:
        allowed_formats = "JPEG, PNG, GIF, WebP (images) and MP4, WebM, MOV (videos)"
        raise FileValidationError(
            code=ErrorCode.INVALID_FILE_TYPE,
            message=f"File type '{mime_type}' is not allowed. Supported types: {allowed_formats}.",
        )

    # Check size based on type
    if file_type == FileType.IMAGE:
        max_size = max_image_size
        type_name = "images"
    else:
        max_size = max_video_size
        type_name = "videos"

    if size_bytes > max_size:
        max_mb = max_size / (1024 * 1024)
        actual_mb = size_bytes / (1024 * 1024)
        raise FileValidationError(
            code=ErrorCode.FILE_TOO_LARGE,
            message=f"File size {actual_mb:.1f}MB exceeds maximum allowed {max_mb:.0f}MB for {type_name}.",
        )

    return ValidationResult(
        mime_type=mime_type,
        file_type=file_type,
        size_bytes=size_bytes,
    )
