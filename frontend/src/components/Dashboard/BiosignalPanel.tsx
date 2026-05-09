import { useMemo } from 'react'
import { useNeuroVerseStore } from '../../store/neuroverseStore'

const ROWS: { label: string; keys: string[] }[] = [
  { label: 'EEG SQI', keys: ['eeg', 'EEG', 'eeg_sqi'] },
  { label: 'Physio SQI', keys: ['physio', 'Physio', 'physio_sqi'] },
  { label: 'Gaze SQI', keys: ['gaze', 'Gaze', 'gaze_sqi'] },
  { label: 'Multimodal SQI', keys: ['multimodal', 'Multimodal', 'multimodal_sqi'] },
]

function pickScore(scores: Record<string, number> | undefined, keys: string[]): number | null {
  if (!scores) return null
  for (const k of keys) {
    if (k in scores) return scores[k]
  }
  const lowerMap = Object.fromEntries(
    Object.entries(scores).map(([key, v]) => [key.toLowerCase(), v])
  )
  for (const k of keys) {
    const v = lowerMap[k.toLowerCase()]
    if (v !== undefined) return v
  }
  return null
}

function barColor(score: number): string {
  if (score > 0.7) return 'bg-neuro-success'
  if (score >= 0.4) return 'bg-neuro-warning'
  return 'bg-neuro-danger'
}

function barTextClass(score: number): string {
  if (score > 0.7) return 'text-neuro-success'
  if (score >= 0.4) return 'text-neuro-warning'
  return 'text-neuro-danger'
}

export function BiosignalPanel() {
  const features = useNeuroVerseStore((state) => state.features)
  const safetyState = useNeuroVerseStore((state) => state.safetyState)

  const sqiScores = useMemo(
    () => features?.sqi_scores ?? safetyState?.sqi_scores,
    [features, safetyState]
  )

  return (
    <div className="rounded-lg border border-neuro-border bg-neuro-surface p-3 font-sans">
      <h3 className="mb-2.5 text-sm font-medium text-neuro-text">Signal quality (SQI)</h3>
      <div className="flex flex-col gap-2">
        {ROWS.map(({ label, keys }) => {
          const raw = pickScore(sqiScores, keys)
          const score = raw != null ? Math.min(1, Math.max(0, raw)) : null
          const pct = score != null ? Math.round(score * 100) : null

          return (
            <div key={label} className="grid grid-cols-[6.75rem_1fr_2.5rem] items-center gap-2">
              <span className="text-xs text-neuro-muted">{label}</span>
              <div className="h-2 overflow-hidden rounded-full bg-neuro-bg">
                {score != null ? (
                  <div
                    className={`h-full rounded-full transition-all duration-300 ${barColor(score)}`}
                    style={{ width: `${pct}%` }}
                  />
                ) : (
                  <div className="h-full w-full bg-neuro-border/50" />
                )}
              </div>
              <span
                className={`text-right font-mono text-[11px] tabular-nums ${
                  score != null ? barTextClass(score) : 'text-neuro-muted'
                }`}
              >
                {pct != null ? `${pct}%` : '—'}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
