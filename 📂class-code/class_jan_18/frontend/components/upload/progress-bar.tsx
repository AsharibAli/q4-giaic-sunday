"use client";

import { useEffect, useRef, useState } from "react";

import { Progress } from "@/components/ui/progress";

interface UploadProgressBarProps {
  progress: number;
  startTime?: number;
  totalBytes?: number;
  loadedBytes?: number;
}

interface UploadStats {
  timeRemaining: string | null;
  uploadSpeed: string | null;
}

function formatTime(seconds: number): string {
  if (seconds < 60) {
    return `${Math.round(seconds)}s`;
  }
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = Math.round(seconds % 60);
  return `${minutes}m ${remainingSeconds}s`;
}

function formatSpeed(bytesPerSecond: number): string {
  if (bytesPerSecond < 1024) {
    return `${bytesPerSecond.toFixed(0)} B/s`;
  }
  if (bytesPerSecond < 1024 * 1024) {
    return `${(bytesPerSecond / 1024).toFixed(1)} KB/s`;
  }
  return `${(bytesPerSecond / (1024 * 1024)).toFixed(1)} MB/s`;
}

const emptyStats: UploadStats = { timeRemaining: null, uploadSpeed: null };

export function UploadProgressBar({
  progress,
  startTime,
  totalBytes,
  loadedBytes,
}: UploadProgressBarProps) {
  const [stats, setStats] = useState<UploadStats>(emptyStats);
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null);

  useEffect(() => {
    // Clear any existing interval
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }

    // Check if we should be calculating stats
    const shouldCalculate = startTime && totalBytes && loadedBytes &&
      loadedBytes > 0 && progress > 0 && progress < 100;

    if (!shouldCalculate) {
      // Use a microtask to avoid synchronous setState in effect
      queueMicrotask(() => {
        setStats(emptyStats);
      });
      return;
    }

    // Capture values in closure for interval callback
    const capturedStartTime = startTime;
    const capturedTotalBytes = totalBytes;
    const capturedLoadedBytes = loadedBytes;

    const calculateStats = () => {
      const now = Date.now();
      const elapsedMs = now - capturedStartTime;
      const elapsedSeconds = elapsedMs / 1000;

      if (elapsedSeconds <= 0) return;

      const bytesPerSecond = capturedLoadedBytes / elapsedSeconds;
      const remainingBytes = capturedTotalBytes - capturedLoadedBytes;
      const remainingSeconds = remainingBytes / bytesPerSecond;

      setStats({
        uploadSpeed: formatSpeed(bytesPerSecond),
        timeRemaining: remainingSeconds > 0 && remainingSeconds < 86400 ? formatTime(remainingSeconds) : null,
      });
    };

    // Start interval
    intervalRef.current = setInterval(calculateStats, 500);
    // Also run immediately via microtask
    queueMicrotask(calculateStats);

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
        intervalRef.current = null;
      }
    };
  }, [startTime, totalBytes, loadedBytes, progress]);

  return (
    <div className="w-full space-y-2">
      <Progress value={progress} className="h-2" />
      <div className="flex justify-between text-sm text-muted-foreground">
        <span>{progress}% uploaded</span>
        <div className="flex gap-4">
          {stats.uploadSpeed && <span>{stats.uploadSpeed}</span>}
          {stats.timeRemaining && <span>{stats.timeRemaining} remaining</span>}
        </div>
      </div>
    </div>
  );
}
