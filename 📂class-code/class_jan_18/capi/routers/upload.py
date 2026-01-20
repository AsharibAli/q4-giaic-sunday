"""Upload endpoints for file storage."""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from ..config import get_settings
from ..models.upload import (
    BatchUploadResponse,
    Error,
    ErrorCode,
    ErrorResponse,
    FailedUpload,
    UploadedFile,
)
from ..services.storage import StorageError, get_storage_service
from ..utils.file_validator import FileValidationError, validate_file
from ..utils.filename import generate_storage_key

router = APIRouter(prefix="/api", tags=["Upload"])
logger = logging.getLogger(__name__)


@router.post(
    "/upload",
    response_model=UploadedFile,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Validation error"},
        503: {"model": ErrorResponse, "description": "Storage service unavailable"},
    },
)
async def upload_file(file: UploadFile = File(...)) -> UploadedFile:
    """
    Upload a single image or video file.

    Supported formats:
    - Images: JPEG, PNG, GIF, WebP (max 100MB)
    - Videos: MP4, WebM, MOV (max 500MB)
    """
    settings = get_settings()

    # Read file content
    content = await file.read()
    original_filename = file.filename or "unnamed_file"

    logger.info(
        "Upload request received",
        extra={
            "file_name": original_filename,
            "content_type": file.content_type,
            "size_bytes": len(content),
        },
    )

    # Validate file type and size
    try:
        validation = validate_file(
            content=content,
            filename=original_filename,
            max_image_size=settings.max_image_size,
            max_video_size=settings.max_video_size,
        )
    except FileValidationError as e:
        logger.warning(
            "File validation failed",
            extra={
                "file_name": original_filename,
                "error_code": e.code.value,
                "error_message": e.message,
            },
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": {"code": e.code.value, "message": e.message}},
        )

    # Generate unique storage key
    storage_key = generate_storage_key(original_filename)

    # Upload to R2
    storage = get_storage_service()
    try:
        url = storage.upload_file(
            content=content,
            storage_key=storage_key,
            content_type=validation.mime_type,
        )
    except StorageError as e:
        logger.error(
            "Storage upload failed",
            extra={"file_name": original_filename, "error": str(e)},
        )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={
                "error": {
                    "code": ErrorCode.STORAGE_ERROR.value,
                    "message": "Storage service is temporarily unavailable. Please try again later.",
                }
            },
        )

    uploaded_at = datetime.now(timezone.utc)

    logger.info(
        "Upload completed successfully",
        extra={
            "file_name": original_filename,
            "storage_key": storage_key,
            "file_type": validation.file_type.value,
            "size_bytes": validation.size_bytes,
            "timestamp": uploaded_at.isoformat(),
        },
    )

    return UploadedFile(
        storage_key=storage_key,
        original_filename=original_filename,
        file_type=validation.file_type,
        mime_type=validation.mime_type,
        size_bytes=validation.size_bytes,
        uploaded_at=uploaded_at,
        url=url,
    )


@router.post(
    "/upload/batch",
    response_model=BatchUploadResponse,
    status_code=status.HTTP_200_OK,
    responses={
        400: {"model": ErrorResponse, "description": "No valid files provided"},
    },
)
async def upload_batch(files: list[UploadFile] = File(...)) -> BatchUploadResponse:
    """
    Upload multiple files in a single request.

    Each file is validated and uploaded independently.
    Partial success is possible - some files may succeed while others fail.
    """
    settings = get_settings()
    storage = get_storage_service()

    successful: list[UploadedFile] = []
    failed: list[FailedUpload] = []

    logger.info(
        "Batch upload request received",
        extra={"file_count": len(files)},
    )

    for file in files:
        original_filename = file.filename or "unnamed_file"
        content = await file.read()

        try:
            # Validate
            validation = validate_file(
                content=content,
                filename=original_filename,
                max_image_size=settings.max_image_size,
                max_video_size=settings.max_video_size,
            )

            # Generate key and upload
            storage_key = generate_storage_key(original_filename)
            url = storage.upload_file(
                content=content,
                storage_key=storage_key,
                content_type=validation.mime_type,
            )

            uploaded_at = datetime.now(timezone.utc)

            successful.append(
                UploadedFile(
                    storage_key=storage_key,
                    original_filename=original_filename,
                    file_type=validation.file_type,
                    mime_type=validation.mime_type,
                    size_bytes=validation.size_bytes,
                    uploaded_at=uploaded_at,
                    url=url,
                )
            )

            logger.info(
                "Batch item uploaded successfully",
                extra={
                    "file_name": original_filename,
                    "storage_key": storage_key,
                },
            )

        except FileValidationError as e:
            failed.append(
                FailedUpload(
                    filename=original_filename,
                    error=Error(code=e.code, message=e.message),
                )
            )
            logger.warning(
                "Batch item validation failed",
                extra={
                    "file_name": original_filename,
                    "error_code": e.code.value,
                },
            )

        except StorageError as e:
            failed.append(
                FailedUpload(
                    filename=original_filename,
                    error=Error(
                        code=ErrorCode.STORAGE_ERROR,
                        message="Storage service error. Please try again later.",
                    ),
                )
            )
            logger.error(
                "Batch item storage failed",
                extra={"file_name": original_filename, "error": str(e)},
            )

    logger.info(
        "Batch upload completed",
        extra={
            "total": len(files),
            "successful": len(successful),
            "failed": len(failed),
        },
    )

    return BatchUploadResponse(
        successful=successful,
        failed=failed,
        total=len(files),
    )
