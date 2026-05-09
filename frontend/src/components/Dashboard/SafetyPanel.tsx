import { useMemo } from 'react'
import type { SafetyDecisionPayload } from '../../types/events'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

function decisionStyles(decision: SafetyDecisionPayload['decision']): {
  badge: string
  ring: string
} {
  switch (decision) {
    case 'ALLOWED':
      return {
        badge: 'bg-emerald-950/80 text-neuro-success ring-emerald-500/40',
        ring: 'ring-neuro-success/30',
      }
    case 'WAIT':
      return {
        badge: 'bg-amber-950/80 text-neuro-warning ring-amber-500/40',
        ring: 'ring-neuro-warning/30',
      }
    case 'BLOCKED':
      return {
        badge: 'bg-red-950/80 text-neuro-danger ring-red-500/40',
        ring: 'ring-neuro-danger/30',
      }
    case 'ASK':
      return {
        badge: 'bg-blue-950/80 text-blue-400 ring-blue-500/40',
        ring: 'ring-blue-400/30',
      }
    default:
      return {
        badge: 'bg-neuro-bg text-neuro-muted ring-neuro-border',
        ring: 'ring-neuro-border',
      }
  }
}

function safetyLevelLabel(level: SafetyDecisionPayload['safety_level']): string {
  switch (level) {
    case 'normal':
      return 'Normal'
    case 'caution':
      return 'Caution'
    case 'freeze':
      return 'Freeze'
    default:
      return String(level)
  }
}

const LEVELS: SafetyDecisionPayload['safety_level'][] = ['normal', 'caution', 'freeze']

function SafetyLevelIndicator({ level }: { level: SafetyDecisionPayload['safety_level'] }) {
  const idx = LEVELS.indexOf(level)

  return (
    <div
      className="flex w-full gap-1.5"
      role="img"
      aria-label={`Safety level: ${safetyLevelLabel(level)}`}
    >
      {LEVELS.map((lvl, i) => {
        let segmentClass = 'bg-neuro-border/80'
        if (level === 'freeze') {
          segmentClass = 'bg-neuro-danger'
        } else if (level === 'caution') {
          if (i === 0) segmentClass = 'bg-neuro-success/25'
          else if (i === 1) segmentClass = 'bg-neuro-warning'
        } else {
          if (i === 0) segmentClass = 'bg-neuro-success'
        }

        const highlight = i === idx && level !== 'freeze'

        return (
          <div
            key={lvl}
            className={`h-2 flex-1 rounded-sm transition-colors ${segmentClass} ${
              highlight ? 'ring-1 ring-white/25' : ''
            }`}
            title={safetyLevelLabel(lvl)}
          />
        )
      })}
    </div>
  )
}

export function SafetyPanel() {
  const safetyState = useNeuroVerseStore((state) => state.safetyState)

  const confidencePct = useMemo(() => {
    if (!safetyState) return null
    return Math.round(Math.min(100, Math.max(0, safetyState.confidence * 100)))
  }, [safetyState])

  if (!safetyState) {
    return (
      <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans">
        <h3 className="mb-2 text-sm font-medium text-neuro-text">Safety</h3>
        <p className="text-sm text-neuro-muted">Awaiting safety assessment...</p>
      </div>
    )
  }

  const { badge, ring } = decisionStyles(safetyState.decision)

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-4 font-sans">
      <h3 className="mb-3 text-sm font-medium text-neuro-text">Safety</h3>

      <div
        className={`mb-4 inline-flex rounded-lg px-5 py-3 text-2xl font-semibold tracking-wide ring-1 ${badge} ${ring}`}
      >
        {safetyState.decision}
      </div>

      <p className="mb-4 text-sm leading-relaxed text-neuro-text">{safetyState.reason}</p>

      <div className="mb-4">
        <div className="mb-1.5 flex items-center justify-between text-xs text-neuro-muted">
          <span>Confidence</span>
          <span className="font-mono tabular-nums text-neuro-text">
            {confidencePct != null ? `${confidencePct}%` : '—'}
          </span>
        </div>
        <div className="h-2 overflow-hidden rounded-full bg-neuro-bg">
          <div
            className="h-full rounded-full bg-gradient-to-r from-indigo-600 to-neuro-accent transition-all"
            style={{ width: `${confidencePct ?? 0}%` }}
          />
        </div>
      </div>

      <div className="mb-1 flex items-center justify-between gap-2 text-xs text-neuro-muted">
        <span>Safety level</span>
        <span className="font-medium text-neuro-text">
          {safetyLevelLabel(safetyState.safety_level)}
        </span>
      </div>
      <div className="mb-4">
        <SafetyLevelIndicator level={safetyState.safety_level} />
      </div>

      {safetyState.blocked_actions.length > 0 && (
        <div>
          <p className="mb-2 text-xs font-medium uppercase tracking-wide text-neuro-muted">
            Blocked actions
          </p>
          <ul className="space-y-1 border-l-2 border-neuro-danger/45 pl-3">
            {safetyState.blocked_actions.map((action) => (
              <li key={action} className="font-mono text-xs text-neuro-danger">
                {action}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}
