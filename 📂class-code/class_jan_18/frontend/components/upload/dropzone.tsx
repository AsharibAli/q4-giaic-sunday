"use client";

import { useCallback, useState } from "react";
import { Upload, X } from "lucide-react";

import { cn } from "@/lib/utils";
import {
  ALLOWED_TYPES,
  formatFileSize,
  getMaxSizeForType,
  isVideoType,
  MAX_IMAGE_SIZE,
  MAX_VIDEO_SIZE,
} from "@/types/upload";

interface DropzoneProps {
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  disabled?: boolean;
  className?: string;
}

export function Dropzone({
  onFilesSelected,
  multiple = false,
  disabled = false,
  className,
}: DropzoneProps) {
  const [isDragOver, setIsDragOver] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const validateFiles = useCallback((files: FileList | File[]): File[] => {
    const validFiles: File[] = [];
    const errors: string[] = [];

    Array.from(files).forEach((file) => {
      // Check type
      if (!ALLOWED_TYPES.includes(file.type as typeof ALLOWED_TYPES[number])) {
        errors.push(`"${file.name}" has unsupported format. Use JPEG, PNG, GIF, WebP, MP4, WebM, or MOV.`);
        return;
      }

      // Check size
      const maxSize = getMaxSizeForType(file.type);
      if (file.size > maxSize) {
        const maxSizeStr = formatFileSize(maxSize);
        const fileSizeStr = formatFileSize(file.size);
        const typeStr = isVideoType(file.type) ? "videos" : "images";
        errors.push(`"${file.name}" (${fileSizeStr}) exceeds ${maxSizeStr} limit for ${typeStr}.`);
        return;
      }

      validFiles.push(file);
    });

    if (errors.length > 0) {
      setError(errors.join(" "));
    } else {
      setError(null);
    }

    return validFiles;
  }, []);

  const handleDragOver = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      if (!disabled) {
        setIsDragOver(true);
      }
    },
    [disabled]
  );

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragOver(false);
  }, []);

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragOver(false);

      if (disabled) return;

      const files = e.dataTransfer.files;
      if (files.length > 0) {
        const validFiles = validateFiles(files);
        if (validFiles.length > 0) {
          onFilesSelected(multiple ? validFiles : [validFiles[0]]);
        }
      }
    },
    [disabled, multiple, onFilesSelected, validateFiles]
  );

  const handleFileInput = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) {
        const validFiles = validateFiles(files);
        if (validFiles.length > 0) {
          onFilesSelected(multiple ? validFiles : [validFiles[0]]);
        }
      }
      // Reset input to allow selecting the same file again
      e.target.value = "";
    },
    [multiple, onFilesSelected, validateFiles]
  );

  const acceptTypes = ALLOWED_TYPES.join(",");

  return (
    <div className="space-y-2">
      <label
        className={cn(
          "flex flex-col items-center justify-center w-full h-48 border-2 border-dashed rounded-lg cursor-pointer transition-colors",
          isDragOver
            ? "border-primary bg-primary/5"
            : "border-muted-foreground/25 hover:border-primary/50 hover:bg-muted/50",
          disabled && "opacity-50 cursor-not-allowed",
          className
        )}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <div className="flex flex-col items-center justify-center pt-5 pb-6">
          <Upload
            className={cn(
              "w-10 h-10 mb-3",
              isDragOver ? "text-primary" : "text-muted-foreground"
            )}
          />
          <p className="mb-2 text-sm text-muted-foreground">
            <span className="font-semibold">Click to upload</span> or drag and drop
          </p>
          <p className="text-xs text-muted-foreground">
            Images (JPEG, PNG, GIF, WebP) up to {formatFileSize(MAX_IMAGE_SIZE)}
          </p>
          <p className="text-xs text-muted-foreground">
            Videos (MP4, WebM, MOV) up to {formatFileSize(MAX_VIDEO_SIZE)}
          </p>
        </div>
        <input
          type="file"
          className="hidden"
          accept={acceptTypes}
          multiple={multiple}
          disabled={disabled}
          onChange={handleFileInput}
        />
      </label>

      {error && (
        <div className="flex items-start gap-2 p-3 text-sm text-destructive bg-destructive/10 rounded-md">
          <X className="w-4 h-4 mt-0.5 flex-shrink-0" />
          <p>{error}</p>
        </div>
      )}
    </div>
  );
}
