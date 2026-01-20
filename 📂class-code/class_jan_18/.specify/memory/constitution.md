<!--
  SYNC IMPACT REPORT
  ==================
  Version change: 0.0.0 → 1.0.0 (MAJOR - initial constitution)

  Modified principles: N/A (new file)
  Added sections:
    - Core Principles (6 principles)
    - Technology Stack
    - Development Workflow
    - Governance
  Removed sections: N/A

  Templates requiring updates:
    - .specify/templates/plan-template.md - ✅ compatible (Constitution Check section exists)
    - .specify/templates/spec-template.md - ✅ compatible (no changes needed)
    - .specify/templates/tasks-template.md - ✅ compatible (no changes needed)

  Follow-up TODOs: None
-->

# GIAIC DBMS Constitution

## Core Principles

### I. Simplicity First

The system MUST remain simple and focused on its core purpose: storing and retrieving class images and videos. Every feature addition MUST be justified against this principle.

- No premature optimization or over-engineering
- No authentication/authorization in Phase 1 (simple open access)
- Direct uploads without complex workflows
- YAGNI (You Aren't Gonna Need It) strictly enforced

### II. Clear Separation of Concerns

Frontend and backend MUST remain decoupled with well-defined API contracts.

- Frontend (Next.js): UI/UX only, no direct storage access
- Backend (FastAPI): Business logic and R2 integration via boto3
- Storage (Cloudflare R2): Object persistence only
- Changes to one layer MUST NOT require changes to others unless API contracts change

### III. Environment-Based Configuration

All secrets and environment-specific values MUST be externalized.

- R2 credentials MUST be in `.env` files, never committed
- API endpoints MUST be configurable per environment
- `.env.example` MUST be maintained with all required variables (no values)
- Fail fast if required environment variables are missing

### IV. API-First Design

Backend API contracts MUST be defined before implementation begins.

- OpenAPI/Swagger documentation MUST be auto-generated from FastAPI
- API endpoints MUST return consistent JSON response structures
- Error responses MUST include meaningful codes and messages
- File uploads MUST use multipart/form-data with size limits

### V. Defensive File Handling

All file operations MUST validate input and handle failures gracefully.

- MUST validate file types (images: jpg, png, gif, webp; videos: mp4, webm, mov)
- MUST enforce maximum file size limits (configurable)
- MUST sanitize filenames before storage
- MUST return appropriate HTTP status codes for all failure modes
- Failed uploads MUST NOT leave partial files in storage

### VI. Observable Operations

System state MUST be observable through logs and responses.

- All upload/download operations MUST be logged with timestamps
- API responses MUST include operation IDs for traceability
- Errors MUST be logged with full context (not exposed to users)
- Health check endpoint MUST exist at `/health`

## Technology Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| Frontend | Next.js | 16.x | React-based UI with App Router |
| UI Components | shadcn/ui | latest | Pre-built accessible components |
| Styling | Tailwind CSS | 4.x | Utility-first CSS |
| Backend | FastAPI | latest | Async Python API framework |
| Storage SDK | boto3 | latest | S3-compatible SDK for R2 |
| Object Storage | Cloudflare R2 | - | S3-compatible blob storage |
| Package Manager (Python) | uv | latest | Fast dependency management |
| Package Manager (Node) | npm | latest | Frontend dependencies |

## Development Workflow

### Local Development

1. Backend: `cd capi && uv sync && uv run uvicorn main:app --reload`
2. Frontend: `cd frontend && npm install && npm run dev`
3. Both services run concurrently during development

### Code Quality Gates

- Frontend: `npm run lint` MUST pass before commits
- Backend: Type hints MUST be used on all function signatures
- No `# type: ignore` without explanatory comment

### Commit Standards

- Conventional commits format: `type(scope): description`
- Types: feat, fix, docs, refactor, test, chore
- Scope: frontend, backend, storage, config

## Governance

This constitution supersedes all ad-hoc practices. Amendments require:

1. Documented rationale for the change
2. Impact assessment on existing code
3. Version increment following semver:
   - MAJOR: Principle removal or incompatible redefinition
   - MINOR: New principle or significant expansion
   - PATCH: Clarification or wording improvements

All pull requests MUST verify compliance with these principles. Complexity additions MUST be justified in PR descriptions.

**Version**: 1.0.0 | **Ratified**: 2026-01-18 | **Last Amended**: 2026-01-18
