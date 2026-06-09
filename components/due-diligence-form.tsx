"use client"

import { useState } from "react"
import { Rocket, AlertCircle, Target, Users } from "lucide-react"
import { FileUploader } from "@/components/file-uploader"
import { ProcessingState } from "@/components/processing-state"
import { ResultsTabs, type DueDiligenceResult } from "@/components/results-tabs"

export function DueDiligenceForm() {
  const [file, setFile] = useState<File | null>(null)
  const [targetSymbol, setTargetSymbol] = useState("AAPL")
  const [competitors, setCompetitors] = useState("MSFT, GOOGL")

  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [result, setResult] = useState<DueDiligenceResult | null>(null)

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setError(null)

    if (!file) {
      setError("Please upload a CSV or PDF financial document before running due diligence.")
      return
    }
    if (!targetSymbol.trim()) {
      setError("Please enter a target ticker symbol.")
      return
    }

    setLoading(true)
    setResult(null)

    try {
      const formData = new FormData()
      formData.append("file", file)
      formData.append("target_symbol", targetSymbol.trim())
      formData.append("competitors", competitors.trim())

      const res = await fetch("/api/due_diligence", {
        method: "POST",
        body: formData,
      })

      const data = await res.json()

      if (!res.ok) {
        throw new Error(data?.error || `Request failed with status ${res.status}`)
      }

      setResult(data as DueDiligenceResult)
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong while running due diligence.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="glass rounded-2xl p-6 shadow-2xl shadow-black/30 sm:p-8">
        <form onSubmit={handleSubmit} className="space-y-6">
          <FileUploader file={file} onFileChange={setFile} disabled={loading} />

          <div className="grid gap-5 sm:grid-cols-2">
            <div>
              <label htmlFor="target-symbol" className="mb-2 block text-sm font-medium text-foreground">
                Target Ticker Symbol
              </label>
              <div className="relative">
                <Target className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  id="target-symbol"
                  type="text"
                  value={targetSymbol}
                  onChange={(e) => setTargetSymbol(e.target.value.toUpperCase())}
                  disabled={loading}
                  aria-label="Target ticker symbol"
                  placeholder="AAPL"
                  className="w-full rounded-xl border border-border bg-input/60 py-2.5 pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground outline-none transition-colors focus:border-primary focus:ring-2 focus:ring-ring/40 disabled:opacity-50"
                />
              </div>
            </div>

            <div>
              <label htmlFor="competitors" className="mb-2 block text-sm font-medium text-foreground">
                Competitor Tickers
              </label>
              <div className="relative">
                <Users className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
                <input
                  id="competitors"
                  type="text"
                  value={competitors}
                  onChange={(e) => setCompetitors(e.target.value)}
                  disabled={loading}
                  aria-label="Competitor ticker symbols, comma separated"
                  placeholder="MSFT, GOOGL"
                  className="w-full rounded-xl border border-border bg-input/60 py-2.5 pl-9 pr-3 text-sm text-foreground placeholder:text-muted-foreground outline-none transition-colors focus:border-primary focus:ring-2 focus:ring-ring/40 disabled:opacity-50"
                />
              </div>
              <p className="mt-1.5 text-xs text-muted-foreground">Comma-separated list of ticker symbols.</p>
            </div>
          </div>

          {error && (
            <div
              role="alert"
              className="flex items-start gap-3 rounded-xl border border-destructive/40 bg-destructive/10 px-4 py-3 text-sm text-destructive"
            >
              <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="group flex w-full items-center justify-center gap-2 rounded-xl bg-primary px-5 py-3 text-sm font-semibold text-primary-foreground shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 hover:shadow-primary/30 focus:outline-none focus:ring-2 focus:ring-ring/50 disabled:cursor-not-allowed disabled:opacity-60 sm:text-base"
          >
            <Rocket className="h-4 w-4 transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            {loading ? "Running Due Diligence…" : "Run Due Diligence"}
          </button>
        </form>
      </div>

      {loading && <ProcessingState />}
      {!loading && result && <ResultsTabs result={result} />}
    </div>
  )
}
