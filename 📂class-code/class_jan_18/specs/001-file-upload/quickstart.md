# Quickstart: File Upload Feature

**Feature**: 001-file-upload
**Date**: 2026-01-18
**Updated**: 2026-01-19

## Prerequisites

- Docker and Docker Compose (recommended)
- OR for local development:
  - Python 3.12+
  - Node.js 20+
  - uv (Python package manager)
  - npm (Node package manager)
- Cloudflare R2 bucket with API credentials

---

## Option 1: Docker (Recommended)

The easiest way to run the application.

### 1. Configure Environment

```bash
cd GIAIC_DBMS
cp .env.example .env
```

Edit `.env` with your R2 credentials:
```env
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=<your-access-key>
R2_SECRET_ACCESS_KEY=<your-secret-key>
R2_BUCKET_NAME=<your-bucket-name>
R2_PUBLIC_URL=https://<bucket>.r2.dev
```

### 2. Start the Application

```bash
docker-compose up --build
```

### 3. Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Docker Commands

```bash
docker-compose up --build      # Build and start all services
docker-compose up -d           # Start in detached mode (background)
docker-compose down            # Stop all services
docker-compose logs -f         # View logs (follow mode)
docker-compose logs backend    # View backend logs only
docker-compose logs frontend   # View frontend logs only
docker-compose ps              # List running containers
docker-compose restart         # Restart all services
```

---

## Option 2: Local Development

### 1. Backend Configuration

Create `capi/.env`:

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
```

### 2. Frontend Configuration

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 3. Install Dependencies

**Backend:**
```bash
cd capi
uv sync
```

**Frontend:**
```bash
cd frontend
npm install
```

### 4. Start the Application

**Backend (Terminal 1)** - Run from project root:
```bash
cd D:\GIAIC_DBMS
fastapi dev capi/main.py
```

**Frontend (Terminal 2):**
```bash
cd frontend
npm run dev
```

### 5. Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## Verification

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "...", "services": {"r2": "connected"}}
```

### 2. Upload Test (via API)

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test-image.jpg"
```

Expected response:
```json
{
  "storage_key": "uuid/test-image.jpg",
  "original_filename": "test-image.jpg",
  "file_type": "image",
  "mime_type": "image/jpeg",
  "size_bytes": 12345,
  "uploaded_at": "2026-01-18T12:00:00Z",
  "url": "https://bucket.r2.dev/uuid/test-image.jpg"
}
```

### 3. Upload Test (via UI)

1. Open http://localhost:3000
2. Drag and drop an image or video file
3. Observe progress bar during upload
4. Confirm success message with shareable link
5. Click "Copy" to copy the URL to clipboard

---

## Troubleshooting

### R2 Connection Failed

1. Verify credentials in `.env` (Docker) or `capi/.env` (local)
2. Check bucket exists in Cloudflare dashboard
3. Ensure API token has R2 read/write permissions
4. Ensure `R2_ENDPOINT_URL` does NOT include the bucket name

### CORS Errors

1. Verify `CORS_ORIGINS` includes frontend URL
2. Restart backend after changing environment

### File Rejected

1. Check file type is allowed (JPEG, PNG, GIF, WebP, MP4, WebM, MOV)
2. Check file size is within limits (100MB images, 500MB videos)
3. Ensure file is not corrupted

### Import Error: No module named 'capi'

Run the backend from the project root directory:
```bash
cd D:\GIAIC_DBMS
fastapi dev capi/main.py
```

### Docker: Container keeps restarting

Check logs for errors:
```bash
docker-compose logs backend
```

Common issues:
- Missing environment variables
- Invalid R2 credentials
- Port already in use

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check (R2 connectivity) |
| POST | /api/upload | Upload single file |
| POST | /api/upload/batch | Upload multiple files |

See `contracts/openapi.yaml` for full API specification.

---

## Credits

Built with ❤️ by [Asharib Ali](https://asharib.xyz/)
