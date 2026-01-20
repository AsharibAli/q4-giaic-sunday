# Research: File Upload Feature

**Feature**: 001-file-upload
**Date**: 2026-01-18
**Status**: Complete

## Research Topics

### 1. Cloudflare R2 Integration with boto3

**Decision**: Use boto3 with custom endpoint URL for R2 (S3-compatible API)

**Rationale**:
- R2 is fully S3-compatible, boto3 is the standard Python SDK
- boto3 is well-documented, battle-tested, and supports all required operations
- Cloudflare recommends boto3 for Python applications
- Supports multipart uploads for large files (>100MB)

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Cloudflare Python SDK | No official SDK exists; R2 relies on S3 compatibility |
| aioboto3 | Adds async complexity; FastAPI's async upload handling is sufficient |
| httpx direct calls | Would require manual S3 signature implementation |

**Configuration Pattern**:
```python
import boto3

s3_client = boto3.client(
    's3',
    endpoint_url=settings.R2_ENDPOINT_URL,
    aws_access_key_id=settings.R2_ACCESS_KEY_ID,
    aws_secret_access_key=settings.R2_SECRET_ACCESS_KEY,
    region_name='auto'  # R2 uses 'auto' for region
)
```

---

### 2. File Type Validation (Content-Based)

**Decision**: Use `python-magic` library for MIME type detection from file content

**Rationale**:
- Validates actual file content, not just extension (FR-003)
- Prevents malicious files with spoofed extensions
- Well-maintained library with libmagic bindings
- Returns standard MIME types that match our allowed list

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Extension-only check | Easily bypassed; doesn't validate actual content |
| filetype library | Less comprehensive MIME detection than python-magic |
| Manual magic byte checking | Error-prone, incomplete coverage |

**Implementation Pattern**:
```python
import magic

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/gif', 'image/webp'}
ALLOWED_VIDEO_TYPES = {'video/mp4', 'video/webm', 'video/quicktime'}

def validate_file_type(file_content: bytes) -> tuple[bool, str]:
    mime = magic.from_buffer(file_content[:2048], mime=True)
    if mime in ALLOWED_IMAGE_TYPES:
        return True, 'image'
    if mime in ALLOWED_VIDEO_TYPES:
        return True, 'video'
    return False, None
```

---

### 3. Unique Filename Generation

**Decision**: UUID4 prefix + sanitized original filename

**Rationale**:
- Guarantees uniqueness (UUID collision is astronomically unlikely)
- Preserves original filename for user reference
- Simple, no database lookup required
- URL-safe characters only

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Timestamp + random | Less unique, potential race conditions |
| Hash of content | Requires reading entire file before naming; duplicates share name |
| Sequential IDs | Requires database state; not scalable |

**Implementation Pattern**:
```python
import uuid
import re

def generate_storage_key(original_filename: str) -> str:
    # Sanitize: keep only alphanumeric, dots, hyphens, underscores
    safe_name = re.sub(r'[^a-zA-Z0-9._-]', '_', original_filename)
    # Limit length
    safe_name = safe_name[:100]
    # Prepend UUID
    return f"{uuid.uuid4()}/{safe_name}"
```

---

### 4. Upload Progress Tracking

**Decision**: Frontend XMLHttpRequest/fetch with progress events; no server-side progress tracking needed

**Rationale**:
- Browser's `XMLHttpRequest.upload.onprogress` provides accurate byte-level progress
- Fetch API with `ReadableStream` for modern approach
- Server-side progress tracking adds complexity without benefit for direct R2 uploads
- FastAPI receives file, uploads to R2 - client tracks frontend→backend progress

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Server-sent events for progress | Over-engineered; browser already provides progress |
| WebSocket progress updates | Unnecessary complexity for simple uploads |
| Polling endpoint | Inefficient; adds latency |

**Frontend Pattern**:
```typescript
const xhr = new XMLHttpRequest();
xhr.upload.addEventListener('progress', (e) => {
  if (e.lengthComputable) {
    const percent = Math.round((e.loaded / e.total) * 100);
    setProgress(percent);
  }
});
```

---

### 5. FastAPI File Upload Handling

**Decision**: Use `UploadFile` with `python-multipart` for streaming uploads

**Rationale**:
- `UploadFile` provides SpooledTemporaryFile that handles large files without OOM
- Streams to disk if file exceeds memory threshold (default 1MB)
- Native FastAPI support, well-documented
- Supports multiple file uploads via `List[UploadFile]`

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Read entire file to memory | OOM risk with 500MB videos |
| Custom streaming parser | Reinventing the wheel; python-multipart is standard |
| Base64 encoding in JSON | Increases payload size 33%; not suitable for large files |

**Endpoint Pattern**:
```python
from fastapi import UploadFile, File

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    # Validate and upload to R2
```

---

### 6. Shareable URL Generation

**Decision**: Construct public R2 URL directly (if bucket is public) or generate presigned URLs

**Rationale**:
- For Phase 1 (no auth), public bucket URLs are simplest
- Pattern: `https://<bucket>.r2.dev/<storage_key>` for public access
- Presigned URLs available for private buckets if needed later
- No database needed to store URLs - construct from storage key

**Alternatives Considered**:
| Alternative | Why Rejected |
|-------------|--------------|
| Store URLs in database | Unnecessary state; URL is deterministic from key |
| Short URL service | Over-engineering for Phase 1 |
| Presigned URLs only | Adds complexity; public access is fine for student materials |

**Configuration**:
- Public bucket: Direct URL `https://{bucket}.r2.dev/{key}`
- Custom domain: `https://files.example.com/{key}`
- Presigned (private): `s3_client.generate_presigned_url(...)`

---

## Dependencies Summary

### Backend (capi/pyproject.toml)
```toml
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "python-multipart>=0.0.6",
    "boto3>=1.34.0",
    "python-magic>=0.4.27",
    "pydantic>=2.5.0",
    "pydantic-settings>=2.1.0",
]
```

### Frontend (frontend/package.json)
Already has required dependencies:
- React 19, Next.js 16
- shadcn/ui components
- Tailwind CSS 4

No additional frontend dependencies required.

---

## NEEDS CLARIFICATION Resolution

No items marked NEEDS CLARIFICATION in Technical Context. All decisions made based on:
- Constitution requirements
- Industry best practices
- Project constraints (Phase 1 simplicity)
