/**
 * TypeScript types for file upload feature.
 * Matches OpenAPI schema from specs/001-file-upload/contracts/openapi.yaml
 */

export type FileType = "image" | "video";

export interface UploadedFile {
  storage_key: string;
  original_filename: string;
  file_type: FileType;
  mime_type: string;
  size_bytes: number;
  uploaded_at: string;
  url: string;
}

export type ErrorCode =
  | "INVALID_FILE_TYPE"
  | "FILE_TOO_LARGE"
  | "STORAGE_ERROR"
  | "VALIDATION_ERROR";

export interface ApiError {
  code: ErrorCode;
  message: string;
}

export interface ErrorResponse {
  error: ApiError;
}

export interface FailedUpload {
  filename: string;
  error: ApiError;
}

export interface BatchUploadResponse {
  successful: UploadedFile[];
  failed: FailedUpload[];
  total: number;
}

export type HealthStatus = "healthy" | "unhealthy";
export type R2Status = "connected" | "disconnected";

export interface HealthResponse {
  status: HealthStatus;
  timestamp: string;
  services?: {
    r2: R2Status;
  };
}

// Frontend-specific types
export type UploadStatus =
  | "idle"
  | "selected"
  | "validating"
  | "uploading"
  | "success"
  | "error";

export interface FileWithStatus {
  file: File;
  id: string;
  status: UploadStatus;
  progress: number;
  error?: string;
  result?: UploadedFile;
}

// Allowed file types
export const ALLOWED_IMAGE_TYPES = [
  "image/jpeg",
  "image/png",
  "image/gif",
  "image/webp",
] as const;

export const ALLOWED_VIDEO_TYPES = [
  "video/mp4",
  "video/webm",
  "video/quicktime",
] as const;

export const ALLOWED_TYPES = [
  ...ALLOWED_IMAGE_TYPES,
  ...ALLOWED_VIDEO_TYPES,
] as const;

// File size limits (in bytes)
export const MAX_IMAGE_SIZE = 100 * 1024 * 1024; // 100MB
export const MAX_VIDEO_SIZE = 500 * 1024 * 1024; // 500MB

export function isImageType(mimeType: string): boolean {
  return ALLOWED_IMAGE_TYPES.includes(mimeType as typeof ALLOWED_IMAGE_TYPES[number]);
}

export function isVideoType(mimeType: string): boolean {
  return ALLOWED_VIDEO_TYPES.includes(mimeType as typeof ALLOWED_VIDEO_TYPES[number]);
}

export function getMaxSizeForType(mimeType: string): number {
  return isVideoType(mimeType) ? MAX_VIDEO_SIZE : MAX_IMAGE_SIZE;
}

export function formatFileSize(bytes: number): string {
  if (bytes === 0) return "0 Bytes";
  const k = 1024;
  const sizes = ["Bytes", "KB", "MB", "GB"];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
}
