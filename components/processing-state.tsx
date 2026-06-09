"use client"

import { Loader2 } from "lucide-react"

const STAGES = ["Ingestion", "Analysis", "Market", "Risk", "Memo"]

export function ProcessingState() {
  return (
    <div
      role="status"
      aria-busy="true"
      aria-live="polite"
      className="flex flex-col items-center gap-6 rounded-2xl border border-border bg-card/60 px-6 py-12 text-center"
    >
      <span className="flex h-14 w-14 items-center justify-center rounded-full bg-primary/15 text-primary">
        <Loader2 className="h-7 w-7 animate-spin" />
      </span>

      <div className="space-y-1.5">
        <p className="text-base font-semibold text-foreground">Agents are processing…</p>
        <p className="text-sm text-muted-foreground">
          Running the autonomous due diligence pipeline. This can take a moment.
        </p>
      </div>

      <div className="flex flex-wrap items-center justify-center gap-2">
        {STAGES.map((stage, i) => (
          <div key={stage} className="flex items-center gap-2">
            <span
              className="rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-medium text-primary animate-pulse-soft"
              style={{ animationDelay: `${i * 0.25}s` }}
            >
              {stage}
            </span>
            {i < STAGES.length - 1 && <span className="text-muted-foreground">{"→"}</span>}
          </div>
        ))}
      </div>
    </div>
  )
}
