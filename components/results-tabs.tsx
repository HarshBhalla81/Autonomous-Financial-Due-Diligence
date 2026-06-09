"use client"

import { useState } from "react"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { FileText, BarChart3, Globe, ShieldAlert, AlertTriangle } from "lucide-react"
import { cn } from "@/lib/utils"
import { CopyButton } from "@/components/copy-button"
import { JsonViewer } from "@/components/json-viewer"

export interface DueDiligenceResult {
  final_memo?: string
  risk_assessment?: string
  financial_metrics?: unknown
  market_intelligence?: unknown
  parsed_document?: unknown
  errors?: string[]
  [key: string]: unknown
}

type TabKey = "memo" | "metrics" | "market"

const TABS: { key: TabKey; label: string; icon: typeof FileText }[] = [
  { key: "memo", label: "Final Investment Memo", icon: FileText },
  { key: "metrics", label: "Financial Metrics", icon: BarChart3 },
  { key: "market", label: "Market Intelligence", icon: Globe },
]

export function ResultsTabs({ result }: { result: DueDiligenceResult }) {
  const [active, setActive] = useState<TabKey>("memo")

  const memo = result.final_memo?.trim() || "_No investment memo was returned by the agents._"
  const metricsJson = JSON.stringify(result.financial_metrics ?? {}, null, 2)
  const marketJson = JSON.stringify(result.market_intelligence ?? {}, null, 2)

  return (
    <section aria-label="Due diligence results" className="animate-fade-in-up space-y-4">
      {result.errors && result.errors.length > 0 && (
        <div className="flex items-start gap-3 rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive">
          <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
          <div>
            <p className="font-medium">Some agents reported issues:</p>
            <ul className="mt-1 list-inside list-disc space-y-0.5 text-destructive/90">
              {result.errors.map((e, i) => (
                <li key={i}>{e}</li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Tab bar */}
      <div
        role="tablist"
        aria-label="Result sections"
        className="flex flex-wrap gap-1 rounded-xl border border-border bg-card/60 p-1"
      >
        {TABS.map(({ key, label, icon: Icon }) => (
          <button
            key={key}
            role="tab"
            aria-selected={active === key}
            aria-controls={`panel-${key}`}
            id={`tab-${key}`}
            onClick={() => setActive(key)}
            className={cn(
              "flex flex-1 items-center justify-center gap-2 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors",
              active === key
                ? "bg-primary text-primary-foreground shadow-sm"
                : "text-muted-foreground hover:bg-input/70 hover:text-foreground",
            )}
          >
            <Icon className="h-4 w-4" />
            <span className="hidden sm:inline">{label}</span>
          </button>
        ))}
      </div>

      {/* Panels */}
      <div className="rounded-2xl border border-border bg-card/60 p-5 sm:p-6">
        {active === "memo" && (
          <div role="tabpanel" id="panel-memo" aria-labelledby="tab-memo" className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <FileText className="h-4 w-4 text-primary" />
                Final Investment Memo
              </h3>
              <CopyButton value={memo} label="Copy memo" />
            </div>

            {result.risk_assessment && (
              <div className="flex items-start gap-3 rounded-xl border border-accent/30 bg-accent/10 px-4 py-3 text-sm">
                <ShieldAlert className="mt-0.5 h-4 w-4 shrink-0 text-accent" />
                <div>
                  <p className="font-medium text-foreground">Risk Assessment</p>
                  <p className="mt-1 text-muted-foreground">{result.risk_assessment}</p>
                </div>
              </div>
            )}

            <article className="prose-memo scrollbar-thin max-h-[34rem] overflow-auto">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{memo}</ReactMarkdown>
            </article>
          </div>
        )}

        {active === "metrics" && (
          <div role="tabpanel" id="panel-metrics" aria-labelledby="tab-metrics" className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <BarChart3 className="h-4 w-4 text-primary" />
                Financial Metrics
              </h3>
              <CopyButton value={metricsJson} label="Copy JSON" />
            </div>
            <JsonViewer data={result.financial_metrics ?? {}} />
          </div>
        )}

        {active === "market" && (
          <div role="tabpanel" id="panel-market" aria-labelledby="tab-market" className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-foreground">
                <Globe className="h-4 w-4 text-primary" />
                Market Intelligence
              </h3>
              <CopyButton value={marketJson} label="Copy JSON" />
            </div>
            <JsonViewer data={result.market_intelligence ?? {}} />
          </div>
        )}
      </div>
    </section>
  )
}
