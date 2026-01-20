# Data Model: File Upload

**Feature**: 001-file-upload
**Date**: 2026-01-18

## Entities

### UploadedFile

Represents a file stored in Cloudflare R2.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| storage_key | string | Unique R2 object key (UUID/filename) | Required, UUID format prefix |
| original_filename | string | User-provided filename | Required, max 255 chars |
| file_type | enum | Category: "image" or "video" | Required, one of allowed values |
| mime_type | string | MIME type (e.g., "image/jpeg") | Required, from allowed list |
| size_bytes | integer | File size in bytes | Required, positive, within limits |
| uploaded_at | datetime | UTC timestamp of upload | Required, ISO 8601 |
| url | string | Shareable URL for the file | Required, valid URL |

**Notes**:
- No database persistence in Phase 1 - entity exists only in API responses
- `storage_key` is the R2 object key, constructed as `{uuid4}/{sanitized_filename}`
- `url` is constructed from bucket configuration + storage_key

### FileType Enum

```
image | video
```

### Allowed MIME Types

**Images** (FR-001):
- `image/jpeg`
- `image/png`
- `image/gif`
- `image/webp`

**Videos** (FR-002):
- `video/mp4`
- `video/webm`
- `video/quicktime` (MOV)

## Validation Rules

### File Size Limits (FR-004)

| File Type | Maximum Size |
|-----------|--------------|
| image | 100 MB (104,857,600 bytes) |
| video | 500 MB (524,288,000 bytes) |

### Filename Sanitization (FR-007)

1. Replace non-alphanumeric characters (except `.`, `-`, `_`) with underscore
2. Truncate to maximum 100 characters
3. Preserve file extension
4. Prepend UUID to ensure uniqueness

**Example**:
- Input: `My Class Photo (2026).jpg`
- Output: `550e8400-e29b-41d4-a716-446655440000/My_Class_Photo__2026_.jpg`

## State Transitions

```
[File Selected] → [Validating] → [Uploading] → [Complete]
                      ↓              ↓
                 [Rejected]     [Failed]
```

| State | Description | Triggers |
|-------|-------------|----------|
| File Selected | User has selected file(s) | File picker or drag-drop |
| Validating | Checking type and size | Before upload starts |
| Rejected | Validation failed | Invalid type or size exceeded |
| Uploading | Transfer in progress | Validation passed |
| Failed | Upload error occurred | Network/storage error |
| Complete | Successfully stored | R2 confirms storage |

## Relationships

```
Frontend                    Backend                   Storage
┌─────────────┐            ┌─────────────┐           ┌─────────┐
│ Upload Form │──upload───▶│ FastAPI     │──put─────▶│ R2      │
│             │◀──response─│ /api/upload │◀──key────│ Bucket  │
└─────────────┘            └─────────────┘           └─────────┘
```

- **Frontend → Backend**: multipart/form-data with file
- **Backend → R2**: boto3 put_object with storage_key
- **Backend → Frontend**: JSON with UploadedFile entity

## API Response Structures

### Success Response

```json
{
  "storage_key": "550e8400-e29b-41d4-a716-446655440000/photo.jpg",
  "original_filename": "My Photo.jpg",
  "file_type": "image",
  "mime_type": "image/jpeg",
  "size_bytes": 1048576,
  "uploaded_at": "2026-01-18T12:00:00Z",
  "url": "https://files.example.com/550e8400-e29b-41d4-a716-446655440000/photo.jpg"
}
```

### Error Response

```json
{
  "error": {
    "code": "INVALID_FILE_TYPE",
    "message": "File type 'application/pdf' is not allowed. Supported types: JPEG, PNG, GIF, WebP (images) and MP4, WebM, MOV (videos)."
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_FILE_TYPE | 400 | File content type not in allowed list |
| FILE_TOO_LARGE | 400 | File exceeds size limit for its type |
| STORAGE_ERROR | 503 | R2 storage unavailable or error |
| VALIDATION_ERROR | 400 | General validation failure |
