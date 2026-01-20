"use client";

import { UploadForm } from "@/components/upload/upload-form";

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-50 dark:bg-black">
      <div className="container max-w-2xl mx-auto py-12 px-4">
        <div className="space-y-8">
          {/* Header */}
          <div className="text-center space-y-2">
            <h1 className="text-3xl font-bold tracking-tight">
              GIAIC Class Media Upload
            </h1>
            <p className="text-muted-foreground">
              Upload your best clicks of GIAIC Sunday 6-9 Class
            </p>
          </div>

          {/* Upload form */}
          <UploadForm mode="single" />

          {/* Footer */}
          <div className="text-center text-sm text-muted-foreground">
            <p>
              Built with ❤️ by{" "}
              <a
                href="https://asharib.xyz/"
                target="_blank"
                rel="noopener noreferrer"
                className="font-medium text-primary hover:underline"
              >
                Asharib Ali
              </a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
