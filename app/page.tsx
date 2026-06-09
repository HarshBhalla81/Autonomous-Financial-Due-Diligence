import { TrendingUp, Sparkles } from "lucide-react"
import { DueDiligenceForm } from "@/components/due-diligence-form"

const PIPELINE = ["Ingestion", "Analysis", "Market", "Risk", "Memo"]

export default function Home() {
  return (
    <main className="mesh-bg min-h-screen">
      {/* Header */}
      <header className="border-b border-border/60">
        <div className="mx-auto flex max-w-5xl flex-col gap-4 px-6 py-10 sm:py-14">
          <div className="flex items-center gap-2 self-start rounded-full border border-primary/30 bg-primary/10 px-3 py-1 text-xs font-medium text-primary">
            <Sparkles className="h-3.5 w-3.5" />
            Multi-agent due diligence pipeline
          </div>

          <div className="flex items-start gap-4">
            <span className="mt-1 flex h-12 w-12 shrink-0 items-center justify-center rounded-2xl bg-primary/15 text-primary">
              <TrendingUp className="h-6 w-6" />
            </span>
            <div className="space-y-2">
              <h1 className="text-pretty text-3xl font-bold tracking-tight text-foreground sm:text-4xl">
                Autonomous Financial Due Diligence
              </h1>
              <p className="max-w-2xl text-pretty text-sm leading-relaxed text-muted-foreground sm:text-base">
                Upload a financial document, point at a target and its competitors, and let autonomous agents
                run the full workflow — ingestion, financial analysis, market intelligence, risk assessment, and
                a final investment memo.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-1">
            {PIPELINE.map((step, i) => (
              <div key={step} className="flex items-center gap-2">
                <span className="rounded-md border border-border bg-card/60 px-2.5 py-1 text-xs font-medium text-muted-foreground">
                  {step}
                </span>
                {i < PIPELINE.length - 1 && <span className="text-xs text-muted-foreground/60">{"→"}</span>}
              </div>
            ))}
          </div>
        </div>
      </header>

      {/* Form + results */}
      <section className="mx-auto w-full max-w-[800px] px-6 py-10 sm:py-12">
        <DueDiligenceForm />
      </section>

      <footer className="border-t border-border/60">
        <div className="mx-auto max-w-5xl px-6 py-6 text-center text-xs text-muted-foreground">
          Powered by a LangGraph multi-agent orchestrator. Outputs are AI-generated and for research purposes only.
        </div>
      </footer>
    </main>
  )
}
