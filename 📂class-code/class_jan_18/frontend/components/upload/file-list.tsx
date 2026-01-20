"use client";

import { File, ImageIcon, Video, X, CheckCircle2, XCircle, Loader2 } from "lucide-react";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { FileWithStatus } from "@/types/upload";
import { formatFileSize, isImageType, isVideoType } from "@/types/upload";

interface FileListProps {
  files: FileWithStatus[];
  onRemove: (id: string) => void;
  disabled?: boolean;
}

function getFileIcon(mimeType: string) {
  if (isImageType(mimeType)) {
    return <ImageIcon className="w-5 h-5" />;
  }
  if (isVideoType(mimeType)) {
    return <Video className="w-5 h-5" />;
  }
  return <File className="w-5 h-5" />;
}

function getStatusIcon(status: FileWithStatus["status"]) {
  switch (status) {
    case "uploading":
      return <Loader2 className="w-4 h-4 animate-spin text-primary" />;
    case "success":
      return <CheckCircle2 className="w-4 h-4 text-green-600" />;
    case "error":
      return <XCircle className="w-4 h-4 text-destructive" />;
    default:
      return null;
  }
}

export function FileList({ files, onRemove, disabled = false }: FileListProps) {
  if (files.length === 0) return null;

  return (
    <div className="space-y-2">
      {files.map((fileItem) => (
        <div
          key={fileItem.id}
          className={cn(
            "flex items-center gap-3 p-3 rounded-lg border bg-card",
            fileItem.status === "error" && "border-destructive/50 bg-destructive/5",
            fileItem.status === "success" && "border-green-200 bg-green-50 dark:border-green-900 dark:bg-green-950"
          )}
        >
          {/* File icon */}
          <div className="text-muted-foreground">
            {getFileIcon(fileItem.file.type)}
          </div>

          {/* File info */}
          <div className="flex-1 min-w-0">
            <p className="font-medium truncate">{fileItem.file.name}</p>
            <p className="text-sm text-muted-foreground">
              {formatFileSize(fileItem.file.size)}
              {fileItem.error && (
                <span className="text-destructive ml-2">• {fileItem.error}</span>
              )}
            </p>
          </div>

          {/* Progress/Status */}
          {fileItem.status === "uploading" && (
            <div className="text-sm text-muted-foreground">
              {fileItem.progress}%
            </div>
          )}
          {getStatusIcon(fileItem.status)}

          {/* Remove button */}
          {!disabled && fileItem.status !== "uploading" && (
            <Button
              variant="ghost"
              size="icon"
              className="h-8 w-8"
              onClick={() => onRemove(fileItem.id)}
            >
              <X className="w-4 h-4" />
              <span className="sr-only">Remove {fileItem.file.name}</span>
            </Button>
          )}
        </div>
      ))}
    </div>
  );
}
