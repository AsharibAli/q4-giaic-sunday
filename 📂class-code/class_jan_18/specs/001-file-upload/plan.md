# Implementation Plan: File Upload

**Branch**: `001-file-upload` | **Date**: 2026-01-18 | **Spec**: [spec.md](./spec.md)
**Status**: ✅ Implemented (2026-01-19)
**Input**: Feature specification from `/specs/001-file-upload/spec.md`

## Summary

Students upload images (JPEG, PNG, GIF, WebP) and videos (MP4, WebM, MOV) through a Next.js frontend that calls a FastAPI backend. The backend validates files, generates unique storage keys, and persists to Cloudflare R2 using boto3. Returns shareable URLs upon success.

## Technical Context

**Language/Version**: Python 3.12 (backend), TypeScript 5.x (frontend)
**Primary Dependencies**: FastAPI, boto3, python-multipart (backend); Next.js 16, React 19, shadcn/ui (frontend)
**Storage**: Cloudflare R2 (S3-compatible object storage)
**Testing**: pytest (backend), Jest/Vitest (frontend) - optional per spec
**Target Platform**: Web browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 50 concurrent uploads, <30s for 10MB files, progress updates every 2s
**Constraints**: 100MB max images, 500MB max videos, no authentication in Phase 1
**Scale/Scope**: Student media uploads for GIAIC class materials

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Simplicity First | No auth, direct uploads, YAGNI | ✅ PASS - No auth, single upload flow |
| II. Clear Separation | Frontend UI only, Backend logic only | ✅ PASS - API boundary defined |
| III. Environment Config | R2 creds in .env, configurable endpoints | ✅ PASS - All secrets externalized |
| IV. API-First Design | OpenAPI docs, consistent JSON, multipart | ✅ PASS - FastAPI auto-generates OpenAPI |
| V. Defensive File Handling | Type/size validation, sanitize names | ✅ PASS - FR-001 to FR-007 cover this |
| VI. Observable Operations | Logging, operation IDs, /health | ✅ PASS - FR-012 requires logging |

**Gate Result**: PASS - All principles satisfied

## Project Structure

### Documentation (this feature)

```text
specs/001-file-upload/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (OpenAPI)
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
capi/                           # FastAPI backend
├── main.py                     # Application entry point, FastAPI app
├── routers/
│   └── upload.py               # Upload endpoints
├── services/
│   └── storage.py              # R2 storage operations via boto3
├── models/
│   └── upload.py               # Pydantic models for request/response
├── utils/
│   ├── file_validator.py       # MIME type and size validation
│   └── filename.py             # Sanitization and unique key generation
├── config.py                   # Environment configuration
└── tests/                      # pytest tests (optional)

frontend/                       # Next.js frontend
├── app/
│   ├── page.tsx                # Main upload page (/)
│   ├── error.tsx               # Error boundary
│   ├── loading.tsx             # Loading state
│   └── upload/
│       └── page.tsx            # Redirects to /
├── components/
│   ├── upload/
│   │   ├── dropzone.tsx        # Drag-and-drop zone
│   │   ├── file-list.tsx       # Selected files display with status
│   │   ├── progress-bar.tsx    # Upload progress with time remaining
│   │   └── upload-form.tsx     # Main upload form (single/batch modes)
│   └── ui/                     # shadcn/ui components (existing)
├── lib/
│   ├── api.ts                  # API client with XMLHttpRequest for progress
│   └── utils.ts                # Existing utilities
└── types/
    └── upload.ts               # TypeScript types matching OpenAPI schema
```

**Structure Decision**: Web application structure with separate `capi/` (backend) and `frontend/` directories. This matches the existing repository layout and constitution principle II (separation of concerns).

## Complexity Tracking

> No constitution violations requiring justification.

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | - | - |
