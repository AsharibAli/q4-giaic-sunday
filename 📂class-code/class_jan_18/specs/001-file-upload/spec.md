# Feature Specification: File Upload

**Feature Branch**: `001-file-upload`
**Created**: 2026-01-18
**Status**: ✅ Implemented
**Updated**: 2026-01-19
**Input**: User description: "Students can upload images and videos to R2 storage via the web interface"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Upload Single Image (Priority: P1)

A student visits the upload page, selects an image file from their device, and uploads it to cloud storage. They receive confirmation that their file was uploaded successfully.

**Why this priority**: This is the core functionality - without single file upload, the entire feature has no value. Images are the most common media type for class materials.

**Independent Test**: Can be fully tested by selecting any image file (jpg, png, gif, webp) and verifying it appears in R2 storage with correct content.

**Acceptance Scenarios**:

1. **Given** a student is on the upload page, **When** they select a valid image file (jpg, png, gif, webp) and click upload, **Then** the file is stored successfully and they see a success confirmation with the filename.
2. **Given** a student has selected an image file, **When** the upload is in progress, **Then** they see a progress indicator showing upload percentage.
3. **Given** a student's upload completes successfully, **When** viewing the confirmation, **Then** they see the stored filename and can copy a shareable link.

---

### User Story 2 - Upload Single Video (Priority: P2)

A student uploads a video file (class recording, tutorial, etc.) to cloud storage. The system handles larger file sizes typical of video content.

**Why this priority**: Videos are essential for class recordings but are secondary to images which are more frequently used. Video uploads require handling larger file sizes.

**Independent Test**: Can be fully tested by selecting any video file (mp4, webm, mov) and verifying it appears in R2 storage.

**Acceptance Scenarios**:

1. **Given** a student is on the upload page, **When** they select a valid video file (mp4, webm, mov) and click upload, **Then** the file is stored successfully and they see a success confirmation.
2. **Given** a student is uploading a large video file, **When** the upload takes longer than a few seconds, **Then** they see continuous progress updates and can see estimated time remaining.

---

### User Story 3 - Upload Multiple Files (Priority: P3)

A student can select and upload multiple files at once, streamlining the process of uploading an entire set of class materials.

**Why this priority**: Bulk upload improves efficiency but is not essential for basic functionality. Students can upload files one at a time as a workaround.

**Independent Test**: Can be fully tested by selecting 3-5 mixed files (images and videos) and verifying all appear in R2 storage.

**Acceptance Scenarios**:

1. **Given** a student is on the upload page, **When** they select multiple valid files and click upload, **Then** all files are uploaded and they see individual status for each file.
2. **Given** a student is uploading multiple files, **When** one file fails validation, **Then** the other valid files still upload successfully and they see clear error messaging for the failed file.

---

### Edge Cases

- What happens when a student uploads a file that exceeds the maximum size limit?
  - System rejects the file before upload begins and displays the maximum allowed size
- What happens when a student's network connection drops during upload?
  - Upload fails gracefully with a retry option; partial uploads are not persisted
- What happens when a student uploads a file with an unsupported format?
  - System rejects the file and displays the list of supported formats
- What happens when a student uploads a file with the same name as an existing file?
  - System generates a unique filename (appending timestamp or UUID) to prevent overwrites
- What happens when R2 storage is temporarily unavailable?
  - System displays a friendly error message asking the student to try again later

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST accept image uploads in formats: JPEG, PNG, GIF, WebP
- **FR-002**: System MUST accept video uploads in formats: MP4, WebM, MOV
- **FR-003**: System MUST validate file type based on content (not just extension) before accepting upload
- **FR-004**: System MUST enforce a maximum file size of 100MB for images and 500MB for videos
- **FR-005**: System MUST display upload progress as a percentage during file transfer
- **FR-006**: System MUST generate unique filenames to prevent collisions
- **FR-007**: System MUST sanitize original filenames to remove special characters before storage
- **FR-008**: System MUST return a shareable URL upon successful upload
- **FR-009**: System MUST display clear error messages for validation failures (wrong format, size exceeded)
- **FR-010**: System MUST support drag-and-drop file selection in addition to file picker
- **FR-011**: System MUST allow cancellation of in-progress uploads
- **FR-012**: System MUST log all upload operations with timestamp and outcome

### Key Entities

- **UploadedFile**: Represents a file stored in R2 storage
  - Original filename (user-provided)
  - Storage key (unique identifier in R2)
  - File type (image or video)
  - MIME type
  - File size in bytes
  - Upload timestamp
  - Shareable URL

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can complete a single file upload in under 30 seconds for files under 10MB on a standard broadband connection
- **SC-002**: 95% of valid file uploads complete successfully on first attempt
- **SC-003**: System provides upload progress feedback that updates at least every 2 seconds during transfer
- **SC-004**: Error messages are displayed within 2 seconds of validation failure
- **SC-005**: System handles at least 50 concurrent uploads without degradation
- **SC-006**: Students can identify and correct upload errors (wrong format, size exceeded) without external help based on error messaging alone

## Assumptions

- No user authentication required for Phase 1 (open access per constitution)
- Students have modern browsers (Chrome, Firefox, Safari, Edge - latest 2 versions)
- Network connectivity is student's responsibility; system only handles graceful failure
- File retention is indefinite unless manually deleted (no auto-expiration in Phase 1)
- Upload quotas per user are not enforced in Phase 1 (no auth = no user tracking)
