# GIAIC Class Media Upload

A web application for GIAIC Sunday 6-9 Class students to upload and share class images and videos. Files are stored securely on Cloudflare R2 and accessible via shareable links.

## Features

- Drag-and-drop file upload interface
- Support for images (JPEG, PNG, GIF, WebP) and videos (MP4, WebM, MOV)
- Real-time upload progress tracking
- Batch upload support (up to 10 files)
- Automatic file type validation
- Shareable public URLs
- Copy-to-clipboard functionality

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 16, React 19, Tailwind CSS v4, shadcn/ui |
| Backend | FastAPI, Python 3.12, Pydantic |
| Storage | Cloudflare R2 (S3-compatible) |
| Package Managers | npm (frontend), uv (backend) |

## How It Works

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Upload Flow                                     │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  User    │────▶│   Frontend   │────▶│   Backend    │────▶│ Cloudflare   │
│  Browser │     │  (Next.js)   │     │  (FastAPI)   │     │     R2       │
└──────────┘     └──────────────┘     └──────────────┘     └──────────────┘
     │                  │                    │                    │
     │  1. Drop file    │                    │                    │
     │─────────────────▶│                    │                    │
     │                  │  2. POST /api/upload                    │
     │                  │───────────────────▶│                    │
     │                  │                    │  3. Validate file  │
     │                  │                    │  (type, size, magic)
     │                  │                    │                    │
     │                  │                    │  4. Upload to R2   │
     │                  │                    │───────────────────▶│
     │                  │                    │                    │
     │                  │                    │  5. Return URL     │
     │                  │                    │◀───────────────────│
     │                  │  6. Return metadata                     │
     │                  │◀───────────────────│                    │
     │  7. Show success │                    │                    │
     │◀─────────────────│                    │                    │
     │                  │                    │                    │
```

### Flow Description

1. **User uploads file** - Drag-and-drop or click to select files
2. **Frontend sends request** - File sent via multipart/form-data to backend
3. **Backend validates** - Checks file extension, MIME type, magic bytes, and size
4. **Upload to R2** - File stored with UUID-prefixed key for uniqueness
5. **R2 confirms** - Storage returns success
6. **Backend responds** - Returns file metadata including public URL
7. **User sees result** - Success message with copyable shareable link

## Prerequisites

- Docker and Docker Compose (recommended)
- OR for local development:
  - Python 3.12+
  - Node.js 20+
  - uv (Python package manager)
  - npm (Node package manager)
- Cloudflare R2 bucket with API credentials

## Quick Start

### Option 1: Docker (Recommended)

The easiest way to run the application.

**1. Configure Environment**

```bash
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

**2. Start the Application**

```bash
docker-compose up --build
```

**3. Access**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Docker Commands**

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

### Option 2: Local Development

**1. Backend Configuration**

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

**2. Frontend Configuration**

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

**3. Install Dependencies**

Backend:
```bash
cd capi
uv sync
```

Frontend:
```bash
cd frontend
npm install
```

**4. Start the Application**

Backend (Terminal 1) - Run from project root:
```bash
cd capi
fastapi dev main.py
```

Frontend (Terminal 2):
```bash
cd frontend
npm run dev
```

**5. Access**

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
GIAIC_DBMS/
├── capi/                      # FastAPI Backend
│   ├── main.py                # Application entry point
│   ├── config.py              # Settings management
│   ├── models/
│   │   └── upload.py          # Pydantic models
│   ├── routers/
│   │   └── upload.py          # Upload endpoints
│   ├── services/
│   │   └── storage.py         # R2 storage service
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/                  # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx           # Main upload page
│   │   └── layout.tsx         # Root layout
│   ├── components/
│   │   └── upload-form.tsx    # Upload form component
│   ├── lib/
│   │   └── api.ts             # API client
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml         # Docker orchestration
├── .env.example               # Environment template
└── README.md
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Service health check (R2 connectivity) |
| POST | `/api/upload` | Upload single file |
| POST | `/api/upload/batch` | Upload multiple files (max 10) |

### Upload Response

```json
{
  "storage_key": "uuid/filename.jpg",
  "original_filename": "filename.jpg",
  "file_type": "image",
  "mime_type": "image/jpeg",
  "size_bytes": 12345,
  "uploaded_at": "2026-01-18T12:00:00Z",
  "url": "https://bucket.r2.dev/uuid/filename.jpg"
}
```

## File Limits

| Type | Max Size | Allowed Formats |
|------|----------|-----------------|
| Images | 100 MB | JPEG, PNG, GIF, WebP |
| Videos | 500 MB | MP4, WebM, MOV |

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

1. Check file type is allowed
2. Check file size is within limits
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

## Verification

### Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy", "timestamp": "...", "services": {"r2": "connected"}}
```

### Upload Test (via API)

```bash
curl -X POST http://localhost:8000/api/upload \
  -F "file=@test-image.jpg"
```

### Upload Test (via UI)

1. Open http://localhost:3000
2. Drag and drop an image or video file
3. Observe progress bar during upload
4. Confirm success message with shareable link
5. Click "Copy" to copy the URL to clipboard

## Credits

Built with ❤️ by [Asharib Ali](https://asharib.xyz/)
