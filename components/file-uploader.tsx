"use client"

import { useCallback, useRef, useState } from "react"
import { UploadCloud, FileText, FileSpreadsheet, X } from "lucide-react"
import { cn } from "@/lib/utils"

interface FileUploaderProps {
  file: File | null
  onFileChange: (file: File | null) => void
  disabled?: boolean
}

const ACCEPTED = ".csv,.pdf"

function formatSize(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function FileUploader({ file, onFileChange, disabled }: FileUploaderProps) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleFiles = useCallback(
    (files: FileList | null) => {
      if (!files || files.length === 0) return
      onFileChange(files[0])
    },
    [onFileChange],
  )

  const onDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      e.stopPropagation()
      setDragActive(false)
      if (disabled) return
      handleFiles(e.dataTransfer.files)
    },
    [disabled, handleFiles],
  )

  const isPdf = file?.name.toLowerCase().endsWith(".pdf")

  return (
    <div>
      <label htmlFor="file-upload" className="mb-2 block text-sm font-medium text-foreground">
        Financial Document
      </label>

      {!file ? (
        <div
          onDragOver={(e) => {
            e.preventDefault()
            if (!disabled) setDragActive(true)
          }}
          onDragLeave={() => setDragActive(false)}
          onDrop={onDrop}
          onClick={() => !disabled && inputRef.current?.click()}
          onKeyDown={(e) => {
            if ((e.key === "Enter" || e.key === " ") && !disabled) inputRef.current?.click()
          }}
          role="button"
          tabIndex={0}
          aria-label="Upload a CSV or PDF financial document"
          className={cn(
            "group flex cursor-pointer flex-col items-center justify-center gap-3 rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors",
            dragActive
              ? "border-primary bg-primary/10"
              : "border-border bg-input/40 hover:border-primary/60 hover:bg-input/70",
            disabled && "cursor-not-allowed opacity-50",
          )}
        >
          <span className="flex h-12 w-12 items-center justify-center rounded-full bg-primary/15 text-primary transition-transform group-hover:scale-105">
            <UploadCloud className="h-6 w-6" />
          </span>
          <div className="space-y-1">
            <p className="text-sm font-medium text-foreground">
              <span className="text-primary">Click to upload</span> or drag &amp; drop
            </p>
            <p className="text-xs text-muted-foreground">CSV or PDF — income statements, filings, reports</p>
          </div>
          <input
            id="file-upload"
            ref={inputRef}
            type="file"
            accept={ACCEPTED}
            className="sr-only"
            disabled={disabled}
            onChange={(e) => handleFiles(e.target.files)}
          />
        </div>
      ) : (
        <div className="flex items-center gap-3 rounded-xl border border-border bg-input/60 px-4 py-3">
          <span
            className={cn(
              "flex h-10 w-10 shrink-0 items-center justify-center rounded-lg",
              isPdf ? "bg-destructive/15 text-destructive" : "bg-accent/15 text-accent",
            )}
          >
            {isPdf ? <FileText className="h-5 w-5" /> : <FileSpreadsheet className="h-5 w-5" />}
          </span>
          <div className="min-w-0 flex-1">
            <p className="truncate text-sm font-medium text-foreground">{file.name}</p>
            <p className="text-xs text-muted-foreground">{formatSize(file.size)}</p>
          </div>
          <button
            type="button"
            onClick={() => {
              onFileChange(null)
              if (inputRef.current) inputRef.current.value = ""
            }}
            disabled={disabled}
            aria-label="Remove file"
            className="flex h-8 w-8 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-destructive/15 hover:text-destructive disabled:opacity-50"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}
    </div>
  )
}
