# Tasks: File Upload

**Input**: Design documents from `/specs/001-file-upload/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Backend**: `capi/` at repository root
- **Frontend**: `frontend/` at repository root

---

## Phase 1: Setup

**Purpose**: Project initialization and environment configuration

- [x] T001 Create backend directory structure: `capi/routers/`, `capi/services/`, `capi/models/`, `capi/utils/`
- [x] T002 Add FastAPI dependencies to `capi/pyproject.toml`: fastapi, uvicorn, python-multipart, boto3, python-magic, pydantic, pydantic-settings
- [x] T003 [P] Create environment configuration in `capi/config.py` with R2 credentials and API settings using pydantic-settings
- [x] T004 [P] Create `.env.example` files in both `capi/.env.example` and `frontend/.env.local.example` with required variables
- [x] T005 [P] Create TypeScript types for upload in `frontend/types/upload.ts` matching OpenAPI schema

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create Pydantic models in `capi/models/upload.py`: UploadedFile, ErrorResponse, Error, HealthResponse
- [x] T007 [P] Implement filename sanitizer and UUID generator in `capi/utils/filename.py`
- [x] T008 [P] Implement file type validator using python-magic in `capi/utils/file_validator.py` with MIME type and size checks
- [x] T009 Implement R2 storage service in `capi/services/storage.py` with upload_file and health_check methods using boto3
- [x] T010 Create health check endpoint `GET /health` in `capi/main.py` that checks R2 connectivity
- [x] T011 Configure FastAPI app in `capi/main.py` with CORS middleware for frontend origin
- [x] T012 [P] Create API client module in `frontend/lib/api.ts` with uploadFile function supporting progress callbacks

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Upload Single Image (Priority: P1)

**Goal**: Students can upload a single image file and receive a shareable URL

**Independent Test**: Select any image file (jpg, png, gif, webp), upload via UI, verify success confirmation with shareable link, confirm file exists in R2

### Implementation for User Story 1

- [x] T013 [US1] Implement single file upload endpoint `POST /api/upload` in `capi/routers/upload.py` handling image types only initially
- [x] T014 [US1] Register upload router in `capi/main.py`
- [x] T015 [P] [US1] Create progress bar component in `frontend/components/upload/progress-bar.tsx` using shadcn/ui Progress
- [x] T016 [P] [US1] Create file dropzone component in `frontend/components/upload/dropzone.tsx` with drag-and-drop support
- [x] T017 [US1] Create upload form component in `frontend/components/upload/upload-form.tsx` integrating dropzone and progress bar
- [x] T018 [US1] Create upload page in `frontend/app/upload/page.tsx` with upload form and success/error state display
- [x] T019 [US1] Update home page `frontend/app/page.tsx` to redirect to /upload or show link to upload page
- [x] T020 [US1] Add copy-to-clipboard functionality for shareable URL in upload success state

**Checkpoint**: User Story 1 complete - single image upload fully functional

---

## Phase 4: User Story 2 - Upload Single Video (Priority: P2)

**Goal**: Students can upload a single video file with larger size limits and see time remaining

**Independent Test**: Select any video file (mp4, webm, mov), upload via UI, verify progress with time estimate, confirm file exists in R2

### Implementation for User Story 2

- [x] T021 [US2] Extend file validator in `capi/utils/file_validator.py` to accept video MIME types with 500MB limit
- [x] T022 [US2] Update upload endpoint in `capi/routers/upload.py` to handle video files with larger size limit
- [x] T023 [US2] Add estimated time remaining calculation to `frontend/components/upload/progress-bar.tsx`
- [x] T024 [US2] Update dropzone in `frontend/components/upload/dropzone.tsx` to accept video file types
- [x] T025 [US2] Update upload form validation messages in `frontend/components/upload/upload-form.tsx` for video size limits

**Checkpoint**: User Story 2 complete - single video upload fully functional (images still work)

---

## Phase 5: User Story 3 - Upload Multiple Files (Priority: P3)

**Goal**: Students can select and upload multiple files at once with individual status per file

**Independent Test**: Select 3-5 mixed files (images and videos), upload all, verify individual success/failure status, confirm all successful files exist in R2

### Implementation for User Story 3

- [x] T026 [US3] Create batch upload endpoint `POST /api/upload/batch` in `capi/routers/upload.py` with BatchUploadResponse
- [x] T027 [US3] Add BatchUploadResponse model to `capi/models/upload.py`
- [x] T028 [P] [US3] Create file list component in `frontend/components/upload/file-list.tsx` showing individual file status
- [x] T029 [US3] Update API client in `frontend/lib/api.ts` with uploadBatch function
- [x] T030 [US3] Update dropzone in `frontend/components/upload/dropzone.tsx` to accept multiple files
- [x] T031 [US3] Update upload form in `frontend/components/upload/upload-form.tsx` to handle multiple files with individual progress
- [x] T032 [US3] Add cancel upload functionality to `frontend/components/upload/upload-form.tsx` using AbortController

**Checkpoint**: User Story 3 complete - batch upload fully functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T033 Add structured logging for all upload operations in `capi/routers/upload.py` with timestamps and outcomes (FR-012)
- [x] T034 [P] Add error boundary and loading states to `frontend/app/upload/page.tsx`
- [x] T035 [P] Create `.env.example` documentation in `capi/README.md` with setup instructions
- [x] T036 Verify all edge cases: oversized file rejection, invalid type rejection, R2 unavailable handling
- [x] T037 Run `npm run lint` in frontend and fix any issues
- [x] T038 Run quickstart.md verification steps to confirm end-to-end functionality

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup
    ↓
Phase 2: Foundational (BLOCKS all user stories)
    ↓
┌───────────────────────────────────────────────┐
│  User stories can proceed in priority order:  │
│  Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3)│
│  OR in parallel if team capacity allows       │
└───────────────────────────────────────────────┘
    ↓
Phase 6: Polish
```

### User Story Dependencies

- **User Story 1 (P1)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on US1 completion (extends existing upload endpoint/UI)
- **User Story 3 (P3)**: Depends on US1 completion (extends to batch uploads)

### Within Each User Story

- Backend endpoint before frontend integration
- Components before page assembly
- Core functionality before enhancements (e.g., progress before time estimate)

### Parallel Opportunities

**Phase 1 (Setup)**:
```
T003 config.py ─┬─ parallel
T004 .env.example ─┤
T005 types/upload.ts ─┘
```

**Phase 2 (Foundational)**:
```
T007 filename.py ─┬─ parallel
T008 file_validator.py ─┤
T012 api.ts ─┘
```

**Phase 3 (US1)**:
```
T015 progress-bar.tsx ─┬─ parallel
T016 dropzone.tsx ─┘
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T012)
3. Complete Phase 3: User Story 1 (T013-T020)
4. **STOP and VALIDATE**: Test single image upload end-to-end
5. Deploy/demo if ready - MVP complete!

### Incremental Delivery

1. Setup + Foundational → Infrastructure ready
2. Add User Story 1 → Test independently → Deploy (MVP!)
3. Add User Story 2 → Test independently → Deploy (videos added)
4. Add User Story 3 → Test independently → Deploy (batch uploads)
5. Polish → Final quality pass

### Task Counts

| Phase | Tasks | Parallelizable |
|-------|-------|----------------|
| Setup | 5 | 3 |
| Foundational | 7 | 3 |
| US1 (P1) | 8 | 2 |
| US2 (P2) | 5 | 0 |
| US3 (P3) | 7 | 1 |
| Polish | 6 | 2 |
| **Total** | **38** | **11** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US2 and US3 extend US1 functionality rather than being fully independent
