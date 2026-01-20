"""Filename sanitization and unique key generation utilities."""

import re
import uuid


def sanitize_filename(filename: str, max_length: int = 100) -> str:
    """
    Sanitize a filename by removing special characters.

    Args:
        filename: Original filename from user
        max_length: Maximum length for the sanitized name

    Returns:
        Sanitized filename safe for storage
    """
    # Replace non-alphanumeric characters (except ., -, _) with underscore
    safe_name = re.sub(r"[^a-zA-Z0-9._-]", "_", filename)

    # Remove consecutive underscores
    safe_name = re.sub(r"_+", "_", safe_name)

    # Remove leading/trailing underscores
    safe_name = safe_name.strip("_")

    # Truncate to max length while preserving extension
    if len(safe_name) > max_length:
        # Find the extension
        parts = safe_name.rsplit(".", 1)
        if len(parts) == 2:
            name, ext = parts
            # Reserve space for extension
            max_name_length = max_length - len(ext) - 1
            safe_name = f"{name[:max_name_length]}.{ext}"
        else:
            safe_name = safe_name[:max_length]

    return safe_name or "unnamed_file"


def generate_storage_key(original_filename: str) -> str:
    """
    Generate a unique storage key for R2.

    Uses UUID4 prefix to guarantee uniqueness while preserving
    the sanitized original filename for reference.

    Args:
        original_filename: Original filename from user

    Returns:
        Unique storage key in format: {uuid}/{sanitized_filename}
    """
    unique_id = uuid.uuid4()
    safe_name = sanitize_filename(original_filename)
    return f"{unique_id}/{safe_name}"
