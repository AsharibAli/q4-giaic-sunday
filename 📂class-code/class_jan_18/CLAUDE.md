# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**GIAIC Class Media Upload** - A web application for GIAIC Sunday 6-9 Class students to upload and share class images and videos.

- **Frontend**: Next.js 16 (React 19) with App Router, Tailwind CSS v4, shadcn/ui components
- **Backend API (capi)**: FastAPI with Python 3.12, using uv for package management
- **Storage**: Cloudflare R2 via boto3 for object storage
- **Containerization**: Docker with docker-compose

## Quick Start (Docker)

The easiest way to run the application:

```bash
# 1. Copy environment template and fill in your R2 credentials
cp .env.example .env

# 2. Start both frontend and backend
docker-compose up --build

# 3. Access the application
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Docker Commands
```bash
docker-compose up --build      # Build and start all services
docker-compose up -d           # Start in detached mode
docker-compose down            # Stop all services
docker-compose logs -f         # View logs
docker-compose ps              # List running containers
```

## Commands (Local Development)

### Frontend (frontend/)
```bash
cd frontend
npm install        # Install dependencies
npm run dev        # Development server at localhost:3000
npm run build      # Production build
npm run start      # Start production server
npm run lint       # Run ESLint
```

### Backend API (capi/)
```bash
cd D:\GIAIC_DBMS                              # Run from project root
fastapi dev capi/main.py                      # Development server with hot reload
# OR
uv run --directory capi uvicorn capi.main:app --reload --port 8000
```

```bash
cd capi
uv sync                                       # Install dependencies
uv add <package>                              # Add a dependency
```

## Architecture

```
├── frontend/                    # Next.js 16 frontend
│   ├── Dockerfile               # Frontend container definition
│   ├── .dockerignore            # Docker build exclusions
│   ├── app/
│   │   ├── page.tsx             # Main upload page (/)
│   │   ├── error.tsx            # Error boundary
│   │   ├── loading.tsx          # Loading state
│   │   └── upload/
│   │       └── page.tsx         # Redirects to /
│   ├── components/
│   │   ├── upload/
│   │   │   ├── dropzone.tsx     # Drag-and-drop file selection
│   │   │   ├── file-list.tsx    # Selected files display with status
│   │   │   ├── progress-bar.tsx # Upload progress with time remaining
│   │   │   └── upload-form.tsx  # Main upload form (single/batch)
│   │   └── ui/                  # shadcn/ui component library
│   ├── lib/
│   │   ├── api.ts               # API client with progress tracking
│   │   └── utils.ts             # Utility functions (cn helper)
│   └── types/
│       └── upload.ts            # TypeScript types matching API
│
├── capi/                        # FastAPI backend
│   ├── Dockerfile               # Backend container definition
│   ├── .dockerignore            # Docker build exclusions
│   ├── __init__.py
│   ├── main.py                  # FastAPI app, CORS, health endpoint
│   ├── config.py                # Environment configuration (pydantic-settings)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── upload.py            # POST /api/upload, POST /api/upload/batch
│   ├── services/
│   │   ├── __init__.py
│   │   └── storage.py           # R2 storage service via boto3
│   ├── models/
│   │   ├── __init__.py
│   │   └── upload.py            # Pydantic models (UploadedFile, BatchUploadResponse)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── file_validator.py    # MIME type validation (python-magic)
│   │   └── filename.py          # Sanitization and UUID key generation
│   ├── .env.example             # Template for environment variables
│   └── pyproject.toml           # Python dependencies (uv managed)
│
├── docker-compose.yml           # Multi-container Docker setup
├── .env.example                 # Docker environment template
│
├── specs/001-file-upload/       # SDD documentation
│   ├── spec.md                  # Feature specification
│   ├── plan.md                  # Implementation plan
│   ├── tasks.md                 # Implementation tasks (all complete)
│   ├── research.md              # Technical decisions
│   ├── data-model.md            # Entity definitions
│   ├── quickstart.md            # Setup instructions
│   └── contracts/
│       └── openapi.yaml         # API specification
│
└── .specify/                    # SDD templates and scripts
```

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /health | Service health check (R2 connectivity) |
| POST | /api/upload | Upload single file (returns UploadedFile) |
| POST | /api/upload/batch | Upload multiple files (returns BatchUploadResponse) |

### Data Flow
1. User selects files via drag-and-drop or file picker on frontend
2. Frontend validates file type/size client-side
3. XMLHttpRequest sends file to FastAPI backend with progress tracking
4. Backend validates file content (python-magic), generates UUID storage key
5. Backend uploads to Cloudflare R2 via boto3
6. Backend returns shareable URL to frontend
7. Frontend displays success with copy-to-clipboard functionality

## Environment Variables

### Docker (.env in project root)
```env
# Cloudflare R2 Configuration
R2_ENDPOINT_URL=https://<account-id>.r2.cloudflarestorage.com
R2_ACCESS_KEY_ID=<your-access-key>
R2_SECRET_ACCESS_KEY=<your-secret-key>
R2_BUCKET_NAME=<your-bucket-name>
R2_PUBLIC_URL=https://<bucket>.r2.dev

# Optional: File Upload Limits (defaults shown)
MAX_IMAGE_SIZE=104857600    # 100MB
MAX_VIDEO_SIZE=524288000    # 500MB
```

### Local Development - Backend (capi/.env)
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

### Local Development - Frontend (frontend/.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Supported File Types

| Type | Formats | Max Size |
|------|---------|----------|
| Images | JPEG, PNG, GIF, WebP | 100MB |
| Videos | MP4, WebM, MOV | 500MB |

## Development Workflow (SDD)

This project uses Spec-Driven Development. Key practices:

### PHR (Prompt History Records)
Create a PHR after completing implementation work in `history/prompts/`:
- Constitution changes → `history/prompts/constitution/`
- Feature work → `history/prompts/<feature-name>/`
- General → `history/prompts/general/`

### ADR (Architecture Decision Records)
When making significant architectural decisions, suggest:
```
📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`
```

### Spec Commands
- `/sp.specify` - Create feature specification
- `/sp.plan` - Generate implementation plan
- `/sp.tasks` - Generate actionable tasks
- `/sp.implement` - Execute implementation plan
- `/sp.adr` - Create Architecture Decision Record

## Project Principles

Defined in `.specify/memory/constitution.md`. Key constraints:
- Never hardcode secrets; use `.env` files
- Prefer smallest viable diff
- No authentication required (Phase 1)
- TDD when applicable
- Ask clarifying questions when requirements are ambiguous

## Credits

Built with ❤️ by [Asharib Ali](https://asharib.xyz/)
