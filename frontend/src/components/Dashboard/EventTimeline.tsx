import { useEffect, useMemo, useRef } from 'react'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const TYPE_STATE = 'neuroverse.state.predicted'
const TYPE_SAFETY = 'neuroverse.safety.decision'
const TYPE_ADAPTATION = 'neuroverse.adaptation.action'

function formatTime(ts: number): string {
  const d = new Date(ts)
  return d.toLocaleTimeString(undefined, {
    hour12: false,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  })
}

function parseSafetyDecision(summary: string): string | null {
  const idx = summary.indexOf(':')
  const head = idx === -1 ? summary.trim() : summary.slice(0, idx).trim()
  if (['ALLOWED', 'BLOCKED', 'WAIT', 'ASK'].includes(head)) return head
  return null
}

function typeBadgeClass(eventType: string, summary: string): string {
  if (eventType === TYPE_STATE) {
    return 'border-blue-500/45 bg-blue-950/55 text-blue-300'
  }
  if (eventType === TYPE_ADAPTATION) {
    return 'border-violet-500/45 bg-violet-950/55 text-violet-300'
  }
  if (eventType === TYPE_SAFETY) {
    const d = parseSafetyDecision(summary)
    if (d === 'ALLOWED') return 'border-emerald-500/45 bg-emerald-950/55 text-neuro-success'
    if (d === 'BLOCKED') return 'border-red-500/45 bg-red-950/55 text-neuro-danger'
    if (d === 'WAIT') return 'border-amber-500/45 bg-amber-950/55 text-neuro-warning'
    if (d === 'ASK') return 'border-sky-500/45 bg-sky-950/55 text-sky-300'
    return 'border-neuro-border bg-neuro-bg text-neuro-muted'
  }
  return 'border-neuro-border bg-neuro-bg text-neuro-muted'
}

function shortType(eventType: string): string {
  if (eventType === TYPE_STATE) return 'state'
  if (eventType === TYPE_SAFETY) return 'safety'
  if (eventType === TYPE_ADAPTATION) return 'adapt'
  const parts = eventType.split('.')
  return parts[parts.length - 1] || eventType
}

export function EventTimeline() {
  const timeline = useNeuroVerseStore((state) => state.timeline)
  const scrollerRef = useRef<HTMLDivElement>(null)

  const rows = useMemo(() => {
    const newestBatch = timeline.slice(0, 20)
    return [...newestBatch].reverse()
  }, [timeline])

  useEffect(() => {
    const el = scrollerRef.current
    if (el) {
      el.scrollTop = el.scrollHeight
    }
  }, [timeline, rows.length])

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-3 font-sans">
      <h3 className="mb-2 text-sm font-medium text-neuro-text">Event timeline</h3>
      <div
        ref={scrollerRef}
        className="max-h-72 overflow-y-auto scroll-smooth rounded-md border border-neuro-border bg-neuro-bg/60 px-2 py-2"
      >
        {rows.length === 0 ? (
          <p className="px-1 py-4 text-center font-mono text-xs text-neuro-muted">No events yet.</p>
        ) : (
          <ul className="space-y-1.5 font-mono text-[11px] leading-snug tracking-tight">
            {rows.map((entry, i) => (
              <li
                key={`${entry.timestamp}-${entry.type}-${i}`}
                className="flex gap-2 border-b border-neuro-border/50 pb-1.5 last:border-0 last:pb-0"
              >
                <span className="shrink-0 tabular-nums text-neuro-muted">{formatTime(entry.timestamp)}</span>
                <span
                  className={`shrink-0 rounded border px-1.5 py-0.5 text-[10px] uppercase tracking-wide ${typeBadgeClass(
                    entry.type,
                    entry.summary
                  )}`}
                >
                  {shortType(entry.type)}
                </span>
                <span className="min-w-0 flex-1 break-words text-neuro-text">{entry.summary}</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
