/**
 * API client for GIAIC DBMS backend.
 */

import type {
  BatchUploadResponse,
  ErrorResponse,
  HealthResponse,
  UploadedFile,
} from "@/types/upload";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Custom error for API failures.
 */
export class ApiError extends Error {
  code: string;

  constructor(code: string, message: string) {
    super(message);
    this.code = code;
    this.name = "ApiError";
  }
}

/**
 * Progress callback type for upload operations.
 */
export type ProgressCallback = (progress: number) => void;

/**
 * Upload a single file to the backend.
 *
 * @param file - File to upload
 * @param onProgress - Optional callback for upload progress (0-100)
 * @param signal - Optional AbortSignal for cancellation
 * @returns Uploaded file metadata
 * @throws ApiError if upload fails
 */
export async function uploadFile(
  file: File,
  onProgress?: ProgressCallback,
  signal?: AbortSignal
): Promise<UploadedFile> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    // Track upload progress
    if (onProgress) {
      xhr.upload.addEventListener("progress", (event) => {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded / event.total) * 100);
          onProgress(percent);
        }
      });
    }

    // Handle completion
    xhr.addEventListener("load", () => {
      if (xhr.status === 201) {
        try {
          const data = JSON.parse(xhr.responseText) as UploadedFile;
          resolve(data);
        } catch {
          reject(new ApiError("VALIDATION_ERROR", "Invalid response from server"));
        }
      } else {
        try {
          const errorData = JSON.parse(xhr.responseText) as ErrorResponse;
          reject(new ApiError(errorData.error.code, errorData.error.message));
        } catch {
          reject(new ApiError("VALIDATION_ERROR", `Upload failed with status ${xhr.status}`));
        }
      }
    });

    // Handle network errors
    xhr.addEventListener("error", () => {
      reject(new ApiError("STORAGE_ERROR", "Network error during upload"));
    });

    // Handle abort
    xhr.addEventListener("abort", () => {
      reject(new ApiError("VALIDATION_ERROR", "Upload cancelled"));
    });

    // Handle abort signal
    if (signal) {
      signal.addEventListener("abort", () => {
        xhr.abort();
      });
    }

    // Prepare and send request
    const formData = new FormData();
    formData.append("file", file);

    xhr.open("POST", `${API_URL}/api/upload`);
    xhr.send(formData);
  });
}

/**
 * Upload multiple files to the backend.
 *
 * @param files - Array of files to upload
 * @param onProgress - Optional callback for overall upload progress (0-100)
 * @param signal - Optional AbortSignal for cancellation
 * @returns Batch upload response with successful and failed uploads
 * @throws ApiError if the entire batch fails
 */
export async function uploadBatch(
  files: File[],
  onProgress?: ProgressCallback,
  signal?: AbortSignal
): Promise<BatchUploadResponse> {
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();

    // Track upload progress
    if (onProgress) {
      xhr.upload.addEventListener("progress", (event) => {
        if (event.lengthComputable) {
          const percent = Math.round((event.loaded / event.total) * 100);
          onProgress(percent);
        }
      });
    }

    // Handle completion
    xhr.addEventListener("load", () => {
      if (xhr.status === 200) {
        try {
          const data = JSON.parse(xhr.responseText) as BatchUploadResponse;
          resolve(data);
        } catch {
          reject(new ApiError("VALIDATION_ERROR", "Invalid response from server"));
        }
      } else {
        try {
          const errorData = JSON.parse(xhr.responseText) as ErrorResponse;
          reject(new ApiError(errorData.error.code, errorData.error.message));
        } catch {
          reject(new ApiError("VALIDATION_ERROR", `Batch upload failed with status ${xhr.status}`));
        }
      }
    });

    // Handle network errors
    xhr.addEventListener("error", () => {
      reject(new ApiError("STORAGE_ERROR", "Network error during upload"));
    });

    // Handle abort
    xhr.addEventListener("abort", () => {
      reject(new ApiError("VALIDATION_ERROR", "Upload cancelled"));
    });

    // Handle abort signal
    if (signal) {
      signal.addEventListener("abort", () => {
        xhr.abort();
      });
    }

    // Prepare and send request
    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });

    xhr.open("POST", `${API_URL}/api/upload/batch`);
    xhr.send(formData);
  });
}

/**
 * Check API health status.
 *
 * @returns Health response with service status
 * @throws ApiError if health check fails
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await fetch(`${API_URL}/health`);

  if (!response.ok) {
    throw new ApiError("STORAGE_ERROR", "Health check failed");
  }

  return response.json() as Promise<HealthResponse>;
}
