# GIAIC DBMS Backend API

FastAPI backend for the GIAIC DBMS file upload service. Handles image and video uploads to Cloudflare R2 storage.

## Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Cloudflare R2 bucket with API credentials

## Setup

1. **Clone and navigate to the backend directory:**
   ```bash
   cd capi
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Configure `.env` with your R2 credentials:**
   ```env
   # Cloudflare R2 Configuration
   R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
   R2_ACCESS_KEY_ID=<your-access-key>
   R2_SECRET_ACCESS_KEY=<your-secret-key>
   R2_BUCKET_NAME=<your-bucket-name>
   R2_PUBLIC_URL=https://<bucket>.r2.dev

   # API Configuration
   API_HOST=0.0.0.0
   API_PORT=8000
   CORS_ORIGINS=http://localhost:3000

   # File Upload Limits (in bytes)
   MAX_IMAGE_SIZE=104857600    # 100MB
   MAX_VIDEO_SIZE=524288000    # 500MB
   ```

4. **Install dependencies:**
   ```bash
   uv sync
   ```

5. **Run the development server:**
   ```bash
   uv run uvicorn capi.main:app --reload
   ```

   The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```
GET /health
```
Returns service health status and R2 connectivity.

### Upload Single File
```
POST /api/upload
Content-Type: multipart/form-data
Body: file (File)
```

**Supported formats:**
- Images: JPEG, PNG, GIF, WebP (max 100MB)
- Videos: MP4, WebM, MOV (max 500MB)

**Response (201 Created):**
```json
{
  "storage_key": "uuid/filename.ext",
  "original_filename": "filename.ext",
  "file_type": "image|video",
  "mime_type": "image/jpeg",
  "size_bytes": 12345,
  "uploaded_at": "2024-01-15T10:30:00Z",
  "url": "https://bucket.r2.dev/uuid/filename.ext"
}
```

### Upload Multiple Files (Batch)
```
POST /api/upload/batch
Content-Type: multipart/form-data
Body: files[] (multiple Files)
```

**Response (200 OK):**
```json
{
  "successful": [...],
  "failed": [
    {
      "filename": "invalid.txt",
      "error": {
        "code": "INVALID_FILE_TYPE",
        "message": "File type not allowed"
      }
    }
  ],
  "total": 5
}
```

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_FILE_TYPE` | File MIME type not in allowed list |
| `FILE_TOO_LARGE` | File exceeds size limit |
| `STORAGE_ERROR` | R2 storage service unavailable |
| `VALIDATION_ERROR` | General validation failure |

## Project Structure

```
capi/
├── config.py           # Environment configuration
├── main.py             # FastAPI app entry point
├── models/
│   └── upload.py       # Pydantic response models
├── routers/
│   └── upload.py       # Upload endpoints
├── services/
│   └── storage.py      # R2 storage service
├── utils/
│   ├── filename.py     # Filename sanitization
│   └── file_validator.py # File validation
├── .env.example        # Environment template
├── pyproject.toml      # Dependencies
└── README.md           # This file
```

## Development

**Run with auto-reload:**
```bash
uv run uvicorn capi.main:app --reload --host 0.0.0.0 --port 8000
```

**Interactive API docs:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Cloudflare R2 Setup

1. Create a Cloudflare account and enable R2
2. Create a new R2 bucket
3. Generate API credentials (R2 API Token with Object Read & Write)
4. Enable public access or configure custom domain for the bucket
5. Copy the endpoint URL, access key, secret key, and public URL to `.env`
