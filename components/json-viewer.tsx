import { cn } from "@/lib/utils"

interface JsonViewerProps {
  data: unknown
}

// Lightweight, dependency-free JSON pretty-printer with dark-mode syntax highlighting.
// (react-json-view is not compatible with React 19, so we render highlighted tokens ourselves.)
function highlight(json: string) {
  const tokenRegex =
    /("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)/g

  const parts: { text: string; cls: string }[] = []
  let lastIndex = 0
  let match: RegExpExecArray | null

  while ((match = tokenRegex.exec(json)) !== null) {
    if (match.index > lastIndex) {
      parts.push({ text: json.slice(lastIndex, match.index), cls: "text-muted-foreground" })
    }
    const token = match[0]
    let cls = "text-accent" // numbers
    if (/^"/.test(token)) {
      cls = /:$/.test(token) ? "text-primary" : "text-foreground"
    } else if (/true|false/.test(token)) {
      cls = "text-accent"
    } else if (/null/.test(token)) {
      cls = "text-destructive"
    }
    parts.push({ text: token, cls })
    lastIndex = tokenRegex.lastIndex
  }
  if (lastIndex < json.length) {
    parts.push({ text: json.slice(lastIndex), cls: "text-muted-foreground" })
  }
  return parts
}

export function JsonViewer({ data }: JsonViewerProps) {
  const json = JSON.stringify(data, null, 2)
  const parts = highlight(json)

  return (
    <pre className="scrollbar-thin max-h-[28rem] overflow-auto rounded-xl border border-border bg-background/60 p-4 font-mono text-xs leading-relaxed">
      <code>
        {parts.map((p, i) => (
          <span key={i} className={cn(p.cls)}>
            {p.text}
          </span>
        ))}
      </code>
    </pre>
  )
}
