"use client";

import { useCallback, useRef, useState } from "react";
import { CheckCircle2, Copy, Loader2, XCircle } from "lucide-react";

import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { uploadFile, uploadBatch, ApiError } from "@/lib/api";
import type { UploadedFile, FileWithStatus, BatchUploadResponse } from "@/types/upload";
import { formatFileSize } from "@/types/upload";
import { Dropzone } from "./dropzone";
import { UploadProgressBar } from "./progress-bar";
import { FileList } from "./file-list";

type UploadMode = "single" | "multiple";

interface UploadFormProps {
  mode?: UploadMode;
}

export function UploadForm({ mode = "single" }: UploadFormProps) {
  const [files, setFiles] = useState<FileWithStatus[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [overallProgress, setOverallProgress] = useState(0);
  const [uploadStartTime, setUploadStartTime] = useState<number | null>(null);
  const [result, setResult] = useState<UploadedFile | null>(null);
  const [batchResult, setBatchResult] = useState<BatchUploadResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);

  const handleFilesSelected = useCallback((selectedFiles: File[]) => {
    const newFiles: FileWithStatus[] = selectedFiles.map((file) => ({
      file,
      id: `${file.name}-${Date.now()}-${Math.random()}`,
      status: "selected",
      progress: 0,
    }));

    if (mode === "single") {
      setFiles(newFiles.slice(0, 1));
    } else {
      setFiles((prev) => [...prev, ...newFiles]);
    }

    // Reset previous results
    setResult(null);
    setBatchResult(null);
    setError(null);
    setOverallProgress(0);
    setCopied(false);
  }, [mode]);

  const handleRemoveFile = useCallback((id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  }, []);

  const handleUpload = useCallback(async () => {
    if (files.length === 0) return;

    setIsUploading(true);
    setError(null);
    setResult(null);
    setBatchResult(null);
    setUploadStartTime(Date.now());
    abortControllerRef.current = new AbortController();

    // Mark all files as uploading
    setFiles((prev) =>
      prev.map((f) => ({ ...f, status: "uploading" as const }))
    );

    if (mode === "single" || files.length === 1) {
      // Single file upload
      const fileToUpload = files[0];

      try {
        const uploaded = await uploadFile(
          fileToUpload.file,
          (progress) => {
            setOverallProgress(progress);
            setFiles((prev) =>
              prev.map((f) =>
                f.id === fileToUpload.id ? { ...f, progress } : f
              )
            );
          },
          abortControllerRef.current.signal
        );

        setResult(uploaded);
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileToUpload.id
              ? { ...f, status: "success", progress: 100, result: uploaded }
              : f
          )
        );
      } catch (err) {
        const message =
          err instanceof ApiError
            ? err.message
            : "Upload failed. Please try again.";
        setError(message);
        setFiles((prev) =>
          prev.map((f) =>
            f.id === fileToUpload.id
              ? { ...f, status: "error", error: message }
              : f
          )
        );
      }
    } else {
      // Batch upload
      try {
        const response = await uploadBatch(
          files.map((f) => f.file),
          (progress) => {
            setOverallProgress(progress);
          },
          abortControllerRef.current.signal
        );

        setBatchResult(response);

        // Update file statuses based on response
        setFiles((prev) =>
          prev.map((f) => {
            const successItem = response.successful.find(
              (s) => s.original_filename === f.file.name
            );
            const failedItem = response.failed.find(
              (s) => s.filename === f.file.name
            );

            if (successItem) {
              return { ...f, status: "success", progress: 100, result: successItem };
            }
            if (failedItem) {
              return { ...f, status: "error", error: failedItem.error.message };
            }
            return f;
          })
        );

        if (response.failed.length > 0 && response.successful.length === 0) {
          setError("All uploads failed. Please check file formats and sizes.");
        }
      } catch (err) {
        const message =
          err instanceof ApiError
            ? err.message
            : "Batch upload failed. Please try again.";
        setError(message);
        setFiles((prev) =>
          prev.map((f) => ({ ...f, status: "error", error: message }))
        );
      }
    }

    setIsUploading(false);
    setUploadStartTime(null);
    abortControllerRef.current = null;
  }, [files, mode]);

  const handleCancel = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
  }, []);

  const handleCopyUrl = useCallback(async (url?: string) => {
    const urlToCopy = url || result?.url;
    if (urlToCopy) {
      try {
        await navigator.clipboard.writeText(urlToCopy);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch {
        // Clipboard API not available
      }
    }
  }, [result?.url]);

  const handleReset = useCallback(() => {
    setFiles([]);
    setResult(null);
    setBatchResult(null);
    setError(null);
    setOverallProgress(0);
    setCopied(false);
  }, []);

  const currentFile = files[0];
  const totalBytes = files.reduce((sum, f) => sum + f.file.size, 0);
  const loadedBytes = Math.round((overallProgress / 100) * totalBytes);
  const hasResults = result || batchResult;

  return (
    <div className="space-y-6">
      {/* Dropzone - hidden when uploading or has result */}
      {!isUploading && !hasResults && (
        <Dropzone
          onFilesSelected={handleFilesSelected}
          multiple={mode === "multiple"}
          disabled={isUploading}
        />
      )}

      {/* Selected files list */}
      {files.length > 0 && !hasResults && (
        <FileList
          files={files}
          onRemove={handleRemoveFile}
          disabled={isUploading}
        />
      )}

      {/* Upload progress */}
      {isUploading && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center gap-3">
                <Loader2 className="w-5 h-5 animate-spin text-primary" />
                <span className="font-medium">
                  Uploading {files.length > 1 ? `${files.length} files` : currentFile?.file.name}...
                </span>
              </div>
              <UploadProgressBar
                progress={overallProgress}
                startTime={uploadStartTime ?? undefined}
                totalBytes={totalBytes}
                loadedBytes={loadedBytes}
              />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success result - single file */}
      {result && !batchResult && (
        <Card className="border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center gap-3 text-green-700 dark:text-green-400">
                <CheckCircle2 className="w-5 h-5" />
                <span className="font-medium">Upload successful!</span>
              </div>

              <div className="space-y-2 text-sm">
                <p>
                  <span className="text-muted-foreground">File:</span>{" "}
                  {result.original_filename}
                </p>
                <p>
                  <span className="text-muted-foreground">Size:</span>{" "}
                  {formatFileSize(result.size_bytes)}
                </p>
                <p>
                  <span className="text-muted-foreground">Type:</span>{" "}
                  {result.mime_type}
                </p>
              </div>

              <div className="flex items-center gap-2">
                <input
                  type="text"
                  value={result.url}
                  readOnly
                  className="flex-1 px-3 py-2 text-sm bg-background border rounded-md"
                />
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => handleCopyUrl()}
                  className="gap-2"
                >
                  <Copy className="w-4 h-4" />
                  {copied ? "Copied!" : "Copy"}
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success result - batch */}
      {batchResult && (
        <div className="space-y-4">
          {batchResult.successful.length > 0 && (
            <Card className="border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950">
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center gap-3 text-green-700 dark:text-green-400">
                    <CheckCircle2 className="w-5 h-5" />
                    <span className="font-medium">
                      {batchResult.successful.length} file(s) uploaded successfully!
                    </span>
                  </div>

                  <div className="space-y-3">
                    {batchResult.successful.map((file) => (
                      <div key={file.storage_key} className="flex items-center gap-2 text-sm">
                        <span className="flex-1 truncate">{file.original_filename}</span>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() => handleCopyUrl(file.url)}
                          className="gap-1 h-7"
                        >
                          <Copy className="w-3 h-3" />
                          Copy URL
                        </Button>
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}

          {batchResult.failed.length > 0 && (
            <Card className="border-destructive/50 bg-destructive/10">
              <CardContent className="pt-6">
                <div className="space-y-4">
                  <div className="flex items-center gap-3 text-destructive">
                    <XCircle className="w-5 h-5" />
                    <span className="font-medium">
                      {batchResult.failed.length} file(s) failed to upload
                    </span>
                  </div>

                  <div className="space-y-2 text-sm">
                    {batchResult.failed.map((file) => (
                      <div key={file.filename} className="text-destructive">
                        <span className="font-medium">{file.filename}:</span> {file.error.message}
                      </div>
                    ))}
                  </div>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Error message */}
      {error && !isUploading && !batchResult && (
        <Card className="border-destructive/50 bg-destructive/10">
          <CardContent className="pt-6">
            <div className="flex items-center gap-3 text-destructive">
              <XCircle className="w-5 h-5" />
              <span>{error}</span>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Action buttons */}
      <div className="flex gap-3">
        {!hasResults && files.length > 0 && (
          <>
            {isUploading ? (
              <Button variant="destructive" onClick={handleCancel}>
                Cancel
              </Button>
            ) : (
              <Button onClick={handleUpload} disabled={files.length === 0}>
                Upload {files.length > 1 ? `${files.length} files` : "file"}
              </Button>
            )}
          </>
        )}

        {(hasResults || error) && (
          <Button variant="outline" onClick={handleReset}>
            Upload more files
          </Button>
        )}
      </div>
    </div>
  );
}
