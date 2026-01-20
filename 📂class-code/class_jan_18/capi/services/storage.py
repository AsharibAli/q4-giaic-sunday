"""R2 storage service using boto3."""

import logging
from functools import lru_cache

import boto3
from botocore.exceptions import ClientError

from ..config import Settings, get_settings

logger = logging.getLogger(__name__)


class StorageError(Exception):
    """Exception raised when storage operations fail."""

    pass


class StorageService:
    """Service for interacting with Cloudflare R2 storage."""

    def __init__(self, settings: Settings):
        """Initialize storage service with settings."""
        self.settings = settings
        self._client = boto3.client(
            "s3",
            endpoint_url=settings.r2_endpoint_url,
            aws_access_key_id=settings.r2_access_key_id,
            aws_secret_access_key=settings.r2_secret_access_key,
            region_name="auto",
        )
        self._bucket = settings.r2_bucket_name

    def upload_file(
        self,
        content: bytes,
        storage_key: str,
        content_type: str,
    ) -> str:
        """
        Upload a file to R2 storage.

        Args:
            content: File content bytes
            storage_key: Unique key for the object
            content_type: MIME type of the file

        Returns:
            Public URL for the uploaded file

        Raises:
            StorageError: If upload fails
        """
        try:
            self._client.put_object(
                Bucket=self._bucket,
                Key=storage_key,
                Body=content,
                ContentType=content_type,
            )
            logger.info(
                "File uploaded successfully",
                extra={
                    "storage_key": storage_key,
                    "content_type": content_type,
                    "size_bytes": len(content),
                },
            )
            return self._build_public_url(storage_key)
        except ClientError as e:
            logger.error(
                "Failed to upload file to R2",
                extra={"storage_key": storage_key, "error": str(e)},
            )
            raise StorageError(f"Failed to upload file: {e}") from e

    def health_check(self) -> bool:
        """
        Check R2 connectivity by listing bucket contents.

        Returns:
            True if R2 is accessible, False otherwise
        """
        try:
            self._client.head_bucket(Bucket=self._bucket)
            return True
        except ClientError as e:
            logger.warning(
                "R2 health check failed",
                extra={"bucket": self._bucket, "error": str(e)},
            )
            return False

    def _build_public_url(self, storage_key: str) -> str:
        """Build public URL for an object."""
        base_url = self.settings.r2_public_url.rstrip("/")
        return f"{base_url}/{storage_key}"


@lru_cache
def get_storage_service() -> StorageService:
    """Get cached storage service instance."""
    return StorageService(get_settings())
